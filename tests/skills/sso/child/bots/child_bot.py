# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import (
    ConversationState,
    TurnContext,
    UserState,
    ActivityHandler,
    ExtendedUserTokenProvider,
)
from botbuilder.dialogs import Dialog, DialogExtensions

from config import DefaultConfig


class ChildBot(ActivityHandler):
    def __init__(
        self,
        config: DefaultConfig,
        main_dialog: Dialog,
        conversation_state: ConversationState,
        user_state: UserState,
    ):
        self._conversation_state = conversation_state
        self._user_state = user_state
        self._main_dialog = main_dialog
        self._connection_name = config.CONNECTION_NAME

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have occurred during the turn.
        await self._conversation_state.save_changes(turn_context)
        await self._user_state.save_changes(turn_context)

    async def on_sign_in_invoke(self, turn_context: TurnContext):
        await self._conversation_state.load(turn_context, True)
        await self._user_state.load(turn_context, True)
        await DialogExtensions.run_dialog(
            self._main_dialog,
            turn_context,
            self._conversation_state.create_property("DialogState"),
        )

    async def on_message_activity(self, turn_context: TurnContext):
        if turn_context.activity.channel_id != "emulator":
            if turn_context.activity.text == "skill login":
                await self._conversation_state.load(turn_context, True)
                await self._user_state.load(turn_context, True)
                await DialogExtensions.run_dialog(
                    self._main_dialog,
                    turn_context,
                    self._conversation_state.create_property("DialogState"),
                )
            elif turn_context.activity.text == "skill logout":
                adapter: ExtendedUserTokenProvider = turn_context.adapter
                await adapter.sign_out_user(
                    turn_context,
                    self._connection_name,
                    turn_context.activity.from_property.id,
                )
                await turn_context.send_activity("logout from child bot successful")
        else:
            await turn_context.send_activity("child: activity (1)")
            await turn_context.send_activity("child: activity (2)")
            await turn_context.send_activity("child: activity (3)")
            await turn_context.send_activity(f"child: {turn_context.activity.text}")
