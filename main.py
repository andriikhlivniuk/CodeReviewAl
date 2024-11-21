from fastapi import FastAPI, HTTPException
from models.request_model import ReviewRequest
from services.github_service import fetch_repo_contents
from services.review_service import generate_code_review

app = FastAPI()

@app.post("/review")
async def review_assignment(request: ReviewRequest):
    
    repo_contents = fetch_repo_contents(str(request.github_repo_url))
    review = generate_code_review(
            repo_contents,
            str(request.assignment_description),
            str(request.candidate_level),
        )
    return review
    # try:
    #     # Step 1: Fetch GitHub repo contents
    #     repo_contents = fetch_repo_contents(str(request.github_repo_url))

    #     # Step 2: Generate code review using GPT API
    #     review = generate_code_review(
    #         repo_contents,
    #         str(request.assignment_description),
    #         str(request.candidate_level),
    #     )

    #     # Step 3: Return the review result
    #     return review

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
