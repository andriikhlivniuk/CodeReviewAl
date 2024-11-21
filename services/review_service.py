import openai
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_code_review(repo_contents, assignment_description, candidate_level):
    # Add validation for empty repo
    if not repo_contents:
        raise Exception("Cannot generate review for empty repository")
    
    logger.info(f"Start generating code review")
    try:
        # Format repository files and their content
        files_and_contents = "\n\n".join(
            [f"File: {filename}\n{content}" for filename, content in repo_contents.items()]
        )

        # Chat messages for OpenAI API
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior software engineer tasked with reviewing code. "
                    "Provide an analysis in the following format:\n\n"
                    "Found Files: List of files in the repository.\n"
                    "Downsides/Comments: Key issues or feedback on the code.\n"
                    "Rating: A score (1-10) based on the code quality.\n"
                    "Conclusion: A summary of your assessment."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Assignment Description: {assignment_description}\n"
                    f"Candidate Level: {candidate_level}\n"
                    f"Repository Code:\n\n{files_and_contents}\n\n"
                    "Please provide a detailed review following the specified format."
                ),
            },
        ]

        # Call the OpenAI ChatCompletion API with updated syntax
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            max_tokens=1500,
            temperature=0.7,
        )

        # Extract and return the content with updated response structure
        return {"review": response.choices[0].message.content.strip()}

    except Exception as e:
        logger.error(f"Failed to generate review: {str(e)}")
        raise Exception(f"Failed to generate code review: {str(e)}")