from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

from ..config import config


questions_agent = Agent(
    name="questions_agent",
    model=Gemini(model=config.model, retry_options=config.retry_config),
    description="Generates interview questions based on the candidate dossier.",
    instruction="""
    You are **Experienced Interviewer**. Your ONLY goal is to generate interview questions based on the candidate dossier.

    **Candidate dossier:**
    {candidate_dossier}

    ### ANALYSIS STEPS:
    1. Analyze the candidate's technical stack, project history, and soft skills.
    2. Identify gaps, vague claims, or impressive achievements that require verification.
    3. Formulate 5 distinct questions.

    ### QUESTION CRITERIA:
    - Mix of Behavioral (STAR method), Technical Deep-dive, and Situational questions.
    - Questions must be open-ended to encourage storytelling.
    - Tailor questions specifically to the candidate's listed projects (e.g., "In your project X...").

    ### OUTPUT FORMAT RULES:
    - Output **ONLY** a raw JSON array of strings.
    - **DO NOT** use Markdown formatting (no ```json or ``` blocks).
    - **DO NOT** include any conversational text, preambles, or explanations.
    - Ensure the JSON is valid and parsable.

    ### OUTPUT EXAMPLE:
    [
        "Question 1",
        "Question 2",
        "Question 3",
        "Question 4",
        "Question 5",
    ]
    """,
    output_key="questions",  # stores output in state['questions']
)
