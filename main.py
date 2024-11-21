from fastapi import FastAPI, HTTPException
from models.request_model import ReviewRequest
from services.github_service import fetch_repo_contents
from services.review_service import generate_code_review

app = FastAPI()

@app.post("/review")
async def review_assignment(request: ReviewRequest):
    try:
        str_github_repo_url = str(request.github_repo_url)
        str_assignment_description = str(request.assignment_description)
        str_candidate_level = str(request.candidate_level)

        # Step 1: Fetch GitHub repo contents
        repo_contents = fetch_repo_contents(str_github_repo_url)

        # Step 2: Generate code review using GPT API
        review = generate_code_review(
            repo_contents,
            str(str_assignment_description),
            str(str_candidate_level),
        )

        return review

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
