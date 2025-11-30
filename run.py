import asyncio
import sys
import os

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from interview_coach.agent import root_agent


# Ensure the current directory is in the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


async def main():
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="app", user_id="user_01", session_id="session_01"
    )

    runner = Runner(agent=root_agent, app_name="app", session_service=session_service)

    print("--- Google ADK Agent Started ---")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("User: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting...")
                break

            print("Agent: ", end="", flush=True)

            async for event in runner.run_async(
                user_id="user_01",
                session_id="session_01",
                new_message=genai_types.Content(
                    role="user", parts=[genai_types.Part.from_text(text=user_input)]
                ),
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    print(event.content.parts[0].text)

            print()

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    asyncio.run(main())
