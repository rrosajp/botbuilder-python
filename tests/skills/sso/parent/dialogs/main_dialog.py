# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    OAuthPrompt,
    OAuthPromptSettings,
)
from botbuilder.schema import TokenResponse

from config import DefaultConfig


class MainDialog(ComponentDialog):
    def __init__(self, config: DefaultConfig):
        super().__init__(MainDialog.__name__)
        self._connection_name = config.CONNECTION_NAME

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__, [self.signin_step, self.show_token_response,]
            )
        )
        self.add_dialog(
            OAuthPrompt(
                OAuthPrompt.__name__,
                OAuthPromptSettings(
                    connection_name=self._connection_name,
                    text="Sign In to AAD",
                    title="Sign In",
                ),
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def signin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.begin_dialog(OAuthPrompt.__name__)

    async def show_token_response(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        result: TokenResponse = step_context.result
        if not result:
            await step_context.context.send_activity(
                "No token response from OAuthPrompt"
            )
        else:
            await step_context.context.send_activity(f"Your token is {result.token}")

        return await step_context.end_dialog()
