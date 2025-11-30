from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_response import LlmResponse


def check_completion_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> LlmResponse:
    """
    Inspects the raw model response for the completion tag.
    """
    if llm_response.content and llm_response.content.parts:
        text = llm_response.content.parts[0].text or ""
        if "[INTERVIEW_COMPLETED]" in text:
            callback_context.state["interview_status"] = "completed"
            # remove the tag from the response as user doesn't need to see it
            llm_response.content.parts[0].text = text.replace(
                "[INTERVIEW_COMPLETED]", ""
            )

    return llm_response
