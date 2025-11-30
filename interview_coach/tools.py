import requests
from bs4 import BeautifulSoup
import os
import pypdf
import json


def scrape_job_offer(url: str) -> dict:
    """
    This function scrapes the text content of a Job Offer from a given URL.
    Use it ONLY if file path given. If pdf file given, read it without this function.

    Args:
        url (str): The URL of the Job Offer to scrape.

    Returns:
        dict: status and result or error msg.
    """
    if not url.startswith("http"):
        return {
            "status": "error",
            "error_message": "Invalid URL. Must start with http:// or https://",
        }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                script.extract()

            text = soup.get_text(separator="\n")

            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_content = "\n".join(chunk for chunk in chunks if chunk)

            return {
                "status": "success",
                "source": url,
                "type": "job_offer_url",
                "content": clean_content[:30000],
            }
        else:
            return {
                "status": "error",
                "error_message": f"Failed to fetch URL. Status code: {response.status_code}",
            }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Scraping error: {str(e)}",
        }


def read_resume_pdf(file_path: str) -> dict:
    """
    This function reads text content from a local PDF Resume file.

    Args:
        file_path (str): The path to the PDF file to read.

    Returns:
        dict: status and result or error msg.
    """
    if not file_path.lower().endswith(".pdf"):
        return {
            "status": "error",
            "error_message": "Invalid file type. Resume must be a .pdf file.",
        }

    if not os.path.exists(file_path):
        return {
            "status": "error",
            "error_message": f"File not found at path: {file_path}",
        }

    try:
        reader = pypdf.PdfReader(file_path)
        extracted_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)

        content = "\n".join(extracted_text)

        if not content.strip():
            return {
                "status": "error",
                "error_message": "PDF found but could not extract text (file might be empty or an image scan).",
            }

        return {
            "status": "success",
            "source": file_path,
            "type": "resume_pdf",
            "content": content[:30000],
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error reading PDF file: {str(e)}",
        }


PROFILE_PATH = "user_profile.json"


def get_stored_resume() -> dict:
    """
    Checks long-term memory (local file) for an existing resume text.

    Returns:
        dict: status and content (or NOT_FOUND).
    """
    if os.path.exists(PROFILE_PATH):
        try:
            with open(PROFILE_PATH, "r") as f:
                data = json.load(f)
                text = data.get("resume_text", "")
                if text:
                    return {
                        "status": "success",
                        "content": text,
                        "message": "Resume loaded from long-term memory.",
                    }
        except Exception as e:
            return {"status": "error", "error_message": f"Corrupt profile file: {e}"}

    return {
        "status": "success",
        "content": "NOT_FOUND",
        "message": "No resume found in memory.",
    }


def save_resume_memory(resume_text: str) -> dict:
    """
    Saves resume text to long-term memory.

    Args:
        resume_text (str): The text content of the resume.

    Returns:
        dict: success status.
    """
    try:
        with open(PROFILE_PATH, "w") as f:
            json.dump({"resume_text": resume_text}, f)
        return {"status": "success", "message": "Resume saved to long-term memory."}
    except Exception as e:
        return {"status": "error", "error_message": f"Failed to save resume: {str(e)}"}
