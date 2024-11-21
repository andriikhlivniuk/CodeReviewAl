from pydantic import BaseModel, HttpUrl, field_validator
from typing import Literal

class ReviewRequest(BaseModel):
    assignment_description: str
    github_repo_url: HttpUrl
    candidate_level: str

    @field_validator('assignment_description')
    @classmethod
    def validate_description(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Assignment description cannot be empty")
        return value.strip()

    @field_validator('github_repo_url')
    @classmethod
    def validate_github_url(cls, value: HttpUrl) -> HttpUrl:
        url_str = str(value)
        if not url_str.startswith(('https://github.com/', 'http://github.com/')):
            raise ValueError("URL must be a GitHub repository URL")
        return value

    @field_validator('candidate_level')
    @classmethod
    def validate_candidate_level(cls, value: str) -> str:
        if value.lower() not in {"junior", "middle", "senior"}:
            raise ValueError("Candidate_level should be: 'junior', 'middle' or 'senior'")
        return value
