import requests

def read_github_file(repo_url, file_path):
    raw_url = repo_url.replace("github.com", "raw.githubusercontent.com") + "/main/" + file_path
    response = requests.get(raw_url)
    response.raise_for_status()
    return response.text
