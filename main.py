from fastapi import FastAPI, HTTPException
from models.request_model import ReviewRequest
from services.github_service import fetch_repo_contents
from services.review_service import generate_code_review
from services.redis_service import cache_get, cache_set

app = FastAPI()

@app.post("/review")
async def review_assignment(request: ReviewRequest):
    try:
        str_github_repo_url = str(request.github_repo_url)
        str_assignment_description = str(request.assignment_description)
        str_candidate_level = str(request.candidate_level)
        
        # Check if Redis is available before cache operations
        cache_key = f"repo:{str_github_repo_url}"
        try:
            cached_contents = cache_get(cache_key)
            if cached_contents:
                return eval(cached_contents)
        except Exception:
            # Redis is not available, continue without caching
            pass

        # Step 1: Fetch GitHub repo contents
        repo_contents = fetch_repo_contents(str_github_repo_url)

        # Step 2: Generate code review using GPT API
        review = generate_code_review(
            repo_contents,
            str_assignment_description,
            str_candidate_level,
        )

        # Cache the results only if Redis is available
        try:
            cache_set(cache_key, str(review))
        except Exception:
            # Redis is not available, skip caching
            pass

        return review

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
