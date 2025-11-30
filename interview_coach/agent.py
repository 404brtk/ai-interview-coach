from google.adk.agents import Agent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.function_tool import FunctionTool

from .config import config
from .tools import get_stored_resume
from .sub_agents import (
    dossier_agent,
    questions_agent,
    interview_conductor_agent,
    critic_agent,
)
from .custom_agents import InterviewWorkflowAgent

setup_pipeline = SequentialAgent(
    name="setup_pipeline",
    description="Generates the dossier and interview questions.",
    sub_agents=[dossier_agent, questions_agent],
)

interview_workflow = InterviewWorkflowAgent(
    name="interview_workflow",
    description="Manages the active interview and final critique.",
    sub_agents=[interview_conductor_agent, critic_agent],
)


root_agent = Agent(
    name="root_agent",
    model=Gemini(model=config.model, retry_options=config.retry_config),
    description="Orchestrates the interview.",
    instruction="""
    You are the **Interview Orchestrator**. Your *ONLY* goal is to manage the lifecycle:
    
    **PHASE 1: PREPARATION**
    Check if the context already contains "questions".
    - If NO:
        1. **Check Memory:** Call `get_stored_resume`.
        2. **If Found:** Ask for Job URL only.
        3. **If Not Found:** Ask for Job URL AND Resume (File/Path/Text).
    
    **PHASE 2: EXECUTION**
    - Once you have the inputs, run `setup_pipeline`.
    - (Note: The agent inside the pipeline will handle reading and saving the resume).

    **PHASE 3: INTERVIEW**
    - If "questions" ARE generated (or `setup_pipeline` just finished), IMMEDIATELY transfer control to `interview_workflow`.
    
    Do not answer interview questions yourself.
    """,
    tools=[
        AgentTool(
            setup_pipeline
        ),  # use setup_pipeline as AgentTool so agents' outputs are ONLY saved to context - don't leave any messages
        FunctionTool(get_stored_resume),
    ],
    sub_agents=[interview_workflow],
)
