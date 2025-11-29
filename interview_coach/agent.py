from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool

from .config import config
from .sub_agents import dossier_agent, questions_agent, interview_conductor_agent


setup_pipeline = SequentialAgent(
    name="setup_pipeline",
    description="Generates the dossier and interview questions.",
    sub_agents=[dossier_agent, questions_agent],
)


root_agent = Agent(
    name="root_agent",
    model=Gemini(model=config.model, retry_options=config.retry_config),
    description="Orchestrates the interview.",
    instruction="""
    You are the **Interview Orchestrator**. Your *ONLY* goal is to manage the lifecycle in two phases:
    
    **PHASE 1: PREPARATION**
    Check if the context already contains "questions".
    - If NO: Ask the user for the Job URL and Resume. Once received, run the `setup_pipeline`.
    
    **PHASE 2: INTERVIEW**
    - If "questions" ARE generated (or `setup_pipeline` just finished), IMMEDIATELY transfer control to `interview_conductor_agent`.
    - For all subsequent user messages (answers to questions), continue delegating to `interview_conductor_agent`.
    
    Do not answer interview questions yourself.
    """,
    tools=[
        AgentTool(setup_pipeline)
    ],  # use setup_pipeline as AgentTool so agents' outputs are ONLY saved to context - don't leave any messages
    sub_agents=[interview_conductor_agent],
)
