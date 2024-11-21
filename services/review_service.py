import openai
import os

# Load API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_code_review(repo_contents, assignment_description, candidate_level):
    try:
        # Create a prompt for GPT to analyze the code
        file_list = [file["name"] for file in repo_contents]
        prompt = (
            f"Assignment Description: {assignment_description}\n"
            f"Candidate Level: {candidate_level}\n"
            f"Repository Files: {', '.join(file_list)}\n"
            f"Please provide a review including downsides, comments, rating, and conclusion."
        )

        # Call OpenAI API
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
        )

        # Parse GPT response
        return {
            "found_files": file_list,
            "downsides_comments": response["choices"][0]["text"].split("\n"),
            "rating": "Good" if "good" in response["choices"][0]["text"].lower() else "Average",
            "conclusion": "Review completed successfully."
        }

    except Exception as e:
        raise Exception(f"Failed to generate code review: {str(e)}")
