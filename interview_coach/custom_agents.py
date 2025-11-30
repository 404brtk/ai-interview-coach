from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator


class InterviewWorkflowAgent(BaseAgent):
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # run the first sub-agent (interviewer)
        interviewer = self.sub_agents[0]
        async for event in interviewer.run_async(ctx):
            yield event

        is_done = ctx.session.state.get("interview_status") == "completed"
        critic_already_ran = ctx.session.state.get("critic_feedback_given", False)

        if is_done and not critic_already_ran:
            # run the second sub-agent (critic)
            critic = self.sub_agents[1]
            async for event in critic.run_async(ctx):
                yield event
            # mark critic feedback as given so we don't repeat it
            ctx.session.state["critic_feedback_given"] = True
        elif is_done and critic_already_ran:
            return  # stop execution
