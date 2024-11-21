
# Code Review Tool

## Overview

This project implements an **Auto-Review Tool** that generates code reviews using **OpenAI's GPT-4 API**. It takes in a set of code files, analyzes them, and provides a detailed review including:
- Found files
- Downsides/Comments
- Rating
- Conclusion

The tool also integrates **Redis** for caching and performance optimization.

---

## Features
- **Code Review Generation**: Analyze multiple files and receive a detailed code review.
- **Error Handling**: Simulate OpenAI API failures and test exception handling.
- **Redis Caching**: Caches responses to improve performance.
- **Testing Suite**: Includes unit tests with Pytest for verifying the tool's functionality and error handling.

---

## Requirements

- Python 3.7+
- OpenAI API key (required to interact with GPT-4)
- Redis (for caching)
- Docker (to run Redis)

---

## Setup Instructions

### 1. Clone the Repository

### 2. Install Dependencies

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the root of the project and add your OpenAI API key:

```plaintext
OPENAI_API_KEY=your-api-key-here
```
---

## Running the Application

### 1. Start the Server

To start the FastAPI server, use the following command:

```bash
uvicorn main:app --reload
```

This will start the server at `http://localhost`.

### 2. Start Redis with Docker

To run Redis and the application in Docker, use:

```bash
docker-compose up --build
```

This will:
- Start a Redis container.


### 3. Access the Endpoint through Swagger UI

```
http://localhost/docs
```

In the Swagger UI, you will see `POST /review` endpoint.

#### Request Body:
You can directly fill out the input for the request body. The `POST /review` endpoint expects the following parameters:

- **assignment_description**: A string describing the coding assignment (e.g., "Build a simple web application").
- **github_repo_url**: The GitHub repository URL to analyze (e.g., `https://github.com/username/repo_name`).
- **candidate_level**: The level of the candidate. Can be:
  - `junior`
  - `mid`
  - `senior`

#### Response:
After filling in the required fields in Swagger UI, click "Execute" to send a request to the server. You will receive a response in the following format:

```json
{
    "review": "Found Files: main.py
Downsides/Comments: No tests
Rating: 7
Conclusion: Good start, but needs tests."
}
```
---

## Running Tests

### 1. Run All Tests

To run the complete test suite:

```bash
pytest
```

### Review Service Tests (`test_review_service.py`)
- Tests code review generation using OpenAI API
- Checks successful review generation with expected format
- Verifies error handling for API failures
- Tests validation of empty repositories

### GitHub Service Tests (`test_github_service.py`)
- Tests GitHub repository content fetching
- Verifies successful file downloads from GitHub
- Checks error handling for non-existent repositories
- Validates correct parsing of repository contents

## What if

For large repositories, I would process files asynchronously to handle multiple files at once without slowing things down. To deal with API rate limits, I’d implement a queuing system with retries for GitHub and OpenAI requests, making sure we don't hit the limits too quickly. I would also keep track of API usage to avoid unexpected costs, setting up alerts or limits to manage expenses effectively.