import requests
import os
from git import Repo

def read_github_file(repo_url, file_path):
    raw_url = repo_url.replace("github.com", "raw.githubusercontent.com") + "/main/" + file_path
    response = requests.get(raw_url)
    response.raise_for_status()
    return response.text

def clone_repo(repo_url, clone_dir):
    if os.path.exists(clone_dir):
        raise FileExistsError("Directory already exists")
    Repo.clone_from(repo_url, clone_dir)

def push_changes(repo, output_file, pat):
    # Stage changes
    repo.git.add(output_file)

    # Commit changes
    repo.git.commit(m='Added summary output')

    # Push changes
    origin = repo.remote(name='origin')
    origin.push(refspec='master', credentials=("token", pat))