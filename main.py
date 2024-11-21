from fastapi import FastAPI, HTTPException
from models.request_model import ReviewRequest
from services.github_service import fetch_repo_contents

app = FastAPI()

@app.post("/review")
async def review_assignment(request: ReviewRequest):
    
    repo_contents = fetch_repo_contents(str(request.github_repo_url))
    return repo_contents
    # try:
    #     # Step 1: Fetch GitHub repo contents
    #     repo_contents = fetch_repo_contents(request.github_repo_url)

    #     # Step 2: Generate code review using GPT API
    #     review = generate_code_review(
    #         repo_contents,
    #         request.assignment_description,
    #         request.candidate_level,
    #     )

    #     # Step 3: Return the review result
    #     return review

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
