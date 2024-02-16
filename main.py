import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html
from config.config import Config
from api.gpt_api import GPTAPI
from utils.github_utils import read_github_file, clone_repo, push_changes
import json
import os
from git import Repo

app = FastAPI()
config = Config()

gpt_api = GPTAPI(config.get_gpt_config().get("api_url"))

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="Your API Description",
        routes=app.routes,
    )
    return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs", redoc_url=None, swagger_js_url="/static/swagger-ui-bundle.js", swagger_css_url="/static/swagger-ui.css")

@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return app.openapi()

@app.get("/generate-summary/")
async def generate_summary(repo_url: str, file_path: str):
    try:
        file_content = read_github_file(repo_url, file_path)
        if file_content:
            prompt = config.get_gpt_config().get("default_prompt", "") + file_content
            max_tokens = config.get_gpt_config().get("default_max_tokens", 50)
            completion = gpt_api.request_completion(prompt, max_tokens)
            if completion:
                summary = completion["choices"][0]["text"].strip()

                # Save the summary to a file
                output_file = "summary_output.json"
                with open(output_file, 'w') as f:
                    json.dump({"summary": summary}, f)

                # Clone the repository
                clone_dir = 'temp_repo'
                clone_repo(repo_url, clone_dir)

                # Commit changes and push to the repository
                repo = Repo(clone_dir)
                pat = os.getenv("GITHUB_PAT")  # Get your PAT from environment variable
                if pat:
                    push_changes(repo, output_file, pat)
                else:
                    print("No GitHub PAT provided. Unable to push changes.")

                # Create a pull request
                # Your code to create a pull request goes here

                return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
