from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from ..config import config


questions_agent = Agent(
    name="questions_agent",
    model=Gemini(model=config.model, retry_options=config.retry_config),
    description="Generates interview questions based on the candidate dossier.",
    instruction="""
    You are **Experienced Interviewer**. Your goal is to generate interview questions based on the candidate dossier.

    Analyze the candidate's background, skills, and experience from the dossier. Create questions that:
    - Assess relevant technical and soft skills for the position
    - Explore specific experiences or projects mentioned in their profile
    - Vary in type (behavioral, technical, situational)
    - Are open-ended to encourage detailed responses

    Generate 5 distinct questions tailored to this candidate.
    OUTPUT EXAMPLE:
    [
        "Question 1",
        "Question 2",
        "Question 3",
        "Question 4",
        "Question 5",
    ]
    """,
    output_key="questions",
)
