from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from .config import config
from .sub_agents import dossier_agent, questions_agent


root_agent = Agent(
    name="root_agent",
    model=Gemini(model=config.model, retry_options=config.retry_config),
    description="Orchestrates the interview process.",
    instruction="""
      You are orchestrating the interview process.
      First call dossier_agent to compile the dossier.
      Then based on the candidate_dossier call questions_agent to generate questions.
      After receiving the questions, you will conduct the interview.

    """,
    sub_agents=[dossier_agent, questions_agent],
)
