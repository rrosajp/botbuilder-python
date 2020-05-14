# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import re
import uuid
from http import HTTPStatus

from botbuilder.core import (
    ActivityHandler,
    ConversationState,
    MessageFactory,
    TurnContext,
    UserState,
    ExtendedUserTokenProvider,
)
from botbuilder.core.card_factory import ContentTypes
from botbuilder.dialogs import DialogExtensions
from botbuilder.integration.aiohttp import BotFrameworkHttpClient
from botbuilder.schema import (
    ActivityTypes,
    Activity,
    TokenExchangeInvokeRequest,
    DeliveryModes,
    ExpectedReplies,
    OAuthCard)
from botframework.connector.token_api.models import TokenExchangeRequest

from config import DefaultConfig
from dialogs import MainDialog


class ParentBot(ActivityHandler):
    MAGIC_CODE_REGEX = "(\\d{6})"

    def __init__(
        self,
        client: BotFrameworkHttpClient,
        config: DefaultConfig,
        main_dialog: MainDialog,
        conversation_state: ConversationState,
        user_state: UserState,
    ):
        self._client = client
        self._conversation_state = conversation_state
        self._user_state = user_state
        self._main_dialog = main_dialog
        self._from_bot_id = config.APP_ID
        self._to_bot_id = config.SKILL_MICROSOFT_APP_ID
        self._connection_name = config.CONNECTION_NAME

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have occurred during the turn.
        await self._conversation_state.save_changes(turn_context)
        await self._user_state.save_changes(turn_context)

    async def on_message_activity(  # pylint: disable=unused-argument
        self, turn_context: TurnContext
    ):
        # for signin, just use an oauth prompt to get the exchangeable token
        # also ensure that the channelId is not emulator
        if turn_context.activity.channel_id != "emulator":
            if (
                re.match(ParentBot.MAGIC_CODE_REGEX, turn_context.activity.text)
                or turn_context.activity.text == "login"
            ):
                # start an oauth prompt
                await self._conversation_state.load(turn_context, True)
                await self._user_state.load(turn_context, True)
                await DialogExtensions.run_dialog(
                    self._main_dialog,
                    turn_context,
                    self._conversation_state.create_property("DialogState"),
                )
            elif turn_context.activity.text == "logout":
                adapter: ExtendedUserTokenProvider = turn_context.adapter
                await adapter.sign_out_user(
                    turn_context,
                    self._connection_name,
                    turn_context.activity.from_property.id,
                )
                await turn_context.send_activity("logout from parent bot successful")
            elif (
                turn_context.activity.text == "skill login"
                or turn_context.activity.text == "skill logout"
            ):
                # incoming activity needs to be cloned for buffered replies
                clone_activity = MessageFactory.text(turn_context.activity.text)
                clone_activity = TurnContext.apply_conversation_reference(
                    clone_activity,
                    TurnContext.get_conversation_reference(turn_context.activity),
                )
                clone_activity.delivery_mode = DeliveryModes.expect_replies

                response1 = await self._client.post_activity(
                    from_bot_id=self._from_bot_id,
                    to_bot_id=self._to_bot_id,
                    to_url="http://localhost:2303/api/messages",
                    service_url="http://tempuri.org/whatever",
                    conversation_id=turn_context.activity.conversation.id,
                    activity=clone_activity,
                )

                if (
                    response1.status == HTTPStatus.OK
                    and response1.body
                ):
                    activities = (
                        ExpectedReplies().deserialize(response1.body).activities
                    )
                    if not await self._intercept_oauth_cards(activities, turn_context):
                        await turn_context.send_activities(activities)

            return

        await turn_context.send_activity("parent: before child")

        activity = MessageFactory.text("parent to child")
        activity = TurnContext.apply_conversation_reference(
            activity, TurnContext.get_conversation_reference(turn_context.activity)
        )
        activity.delivery_mode = DeliveryModes.expect_replies

        response = await self._client.post_activity(
            from_bot_id=self._from_bot_id,
            to_bot_id=self._to_bot_id,
            to_url="http://localhost:2303/api/messages",
            service_url="http://tempuri.org/whatever",
            conversation_id=str(uuid.uuid4()),
            activity=activity,
        )

        if response.status == HTTPStatus.OK:
            activities = ExpectedReplies().deserialize(response.body).activities
            await turn_context.send_activities(activities)

        await turn_context.send_activity("parent: after child")

    async def _intercept_oauth_cards(
        self, activities: [Activity], turn_context: TurnContext
    ) -> bool:
        if not activities:
            return False

        activity = activities[0]

        oauth_card_attachment = next(
            attachment
            for attachment in activity.attachments
            if attachment.content_type == ContentTypes.oauth_card
        )
        if oauth_card_attachment:
            if isinstance(oauth_card_attachment.content, dict):
                oauth_card = OAuthCard().deserialize(oauth_card_attachment.content)
            else:
                oauth_card = oauth_card_attachment.content
            if (
                oauth_card
                and oauth_card.token_exchange_resource
                and oauth_card.token_exchange_resource.uri
            ):
                try:
                    result = await turn_context.adapter.exchange_token(
                        turn_context=turn_context,
                        connection_name=self._connection_name,
                        user_id=turn_context.activity.from_property.id,
                        exchange_request=TokenExchangeRequest(
                            uri=oauth_card.token_exchange_resource.uri
                        ),
                    )

                    if result and result.token:
                        # If token above is null, then SSO has failed and hence we return false.
                        # If not, send an invoke to the skill with the token.
                        return await self._send_token_exchange_invoke_to_skill(
                            turn_context,
                            activity,
                            oauth_card.token_exchange_resource.id,
                            oauth_card.connection_name,
                            result.token,
                        )
                except:
                    # Failures in token exchange are not fatal. They simply mean that the user needs
                    # to be shown the OAuth card.
                    return False

        return False

    async def _send_token_exchange_invoke_to_skill(
        self,
        turn_context: TurnContext,
        incoming_activity: Activity,
        request_id: str,
        connection_name: str,
        token: str,
    ) -> bool:
        activity = incoming_activity.create_reply()
        activity.type = ActivityTypes.invoke
        activity.name = "signin/tokenExchange"
        activity.value = TokenExchangeInvokeRequest(
            id=request_id, token=token, connection_name=connection_name,
        )

        # route the activity to the skill
        response = await self._client.post_activity(
            self._from_bot_id,
            self._to_bot_id,
            "http://localhost:2303/api/messages",
            "http://tempuri.org/whatever",
            incoming_activity.conversation.id,
            activity,
        )

        # Check response status: true if success, false if failure
        success = response.is_successful_status_code()

        if success:
            await turn_context.send_activity("Skill token exchange successful")
        else:
            await turn_context.send_activity("Skill token exchange failed")

        return success
