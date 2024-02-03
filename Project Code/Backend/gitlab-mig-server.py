import select
from flask import Flask, jsonify, request

import os
import requests
from git import Repo
import shutil
import re
import sys
import csv



app = Flask(__name__)

@app.route('/')
def homePage():
    return "WELCOME TO THE MIGRATION PROJECT"

# Clean up the temporary repository directory
def cleanup_temp_repo():
    if os.path.exists("temp_repo"):
        shutil.rmtree("temp_repo")

# Fetch groups and projects from GitLab and save to CSV
def fetch_gitlab_groups_and_projects(gitlab_token, gitlab_api_url, save_to_csv=True):
    headers = {"Authorization": f"Bearer {gitlab_token}"}
    response = requests.get(f"{gitlab_api_url}/groups", headers=headers)
    groups = response.json()

    data = []
    for group in groups:
        group_name = group["name"]
        group_id = group["id"]
        projects_response = requests.get(f"{gitlab_api_url}/groups/{group_id}/projects", headers=headers)
        projects = projects_response.json()
        for project in projects:
            project_name = project["name"]
            project_path = project["path_with_namespace"]
            project_clone_url = f"https://oauth2:{gitlab_token}@gitlab.com/{project_path}.git"
            data.append([group_name, project_name, project_clone_url])
            # project - repo - repoUrl

    if save_to_csv:
        with open("gitlab_projects.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    return data


# Create Bitbucket Cloud project
def create_bitbucket_project(group_name , bitbucket_username , bitbucket_app_password , bitbucket_api_url , workspace):
    auth = (bitbucket_username, bitbucket_app_password)

    # Remove special characters from group_name
    key = re.sub(r'\W+', '', group_name)
    print("=========creating project==========")
    print("Project:", group_name)
    print("===================================")

    data = {"key": key, "name": group_name, "is_private": True}
    response = requests.post(f"{bitbucket_api_url}/workspaces/{workspace}/projects", auth=auth, json=data)
    #print(response.status_code)
    if response.status_code == 400:
        # Project with the same name already exists, skip to the next step
        print("Project already exists. Skipping creation.")
        return
    elif response.status_code not in (200, 201):
        raise Exception("Failed to create Bitbucket project")

    # Project created successfully
    print("Bitbucket project created.")


# Create Bitbucket Cloud repository
def create_bitbucket_repository(group_name, project_name, clone_url, bitbucket_username , bitbucket_app_password , bitbucket_api_url , workspace):
    auth = (bitbucket_username, bitbucket_app_password)

    # Remove special characters from group_name
    key = re.sub(r'\W+', '', group_name)
    print("=========creating repository==========")
    print("Repository Slug:", project_name)
    print("======================================")

    repo_slug = project_name.lower().replace(" ", "-")  # Generate the slug from the project name
    data = {"scm": "git", "is_private": True, "name": project_name, "project": {"key": key}}
    response = requests.post(f"{bitbucket_api_url}/repositories/{workspace}/{repo_slug}", auth=auth, json=data)
    #print(response.text)
    #print(response.status_code)

    if response.status_code == 400:
        # Repository with the same slug already exists, skip to the next step
        print("Repository already exists. Skipping creation.")
        return
    elif response.status_code not in (200, 201):
        raise Exception("Failed to create Bitbucket repository")
    bitbucket_repo_url = response.json()["links"]["clone"][0]["href"]
    clone_and_push_repository(clone_url, bitbucket_repo_url , bitbucket_username, bitbucket_app_password , workspace)


# Clone GitLab repository and push to Bitbucket repository
def clone_and_push_repository(clone_url, bitbucket_repo_url ,bitbucket_username, bitbucket_app_password , workspace):
    # Clone the GitLab repository using the modified clone URL
    print("=========clone and push repository==========")
    print("Repository URL:", bitbucket_repo_url)
    print("============================================")
    repo_dir = "temp_repo"
    repo = Repo.clone_from(clone_url, repo_dir, mirror=True)

    # print("Clone url \n" )
    # https://oauth2:glpat-CexxfdRJWUUmisdCrEQs@gitlab.com/sid-test1-group/Sid-test1-Project.git


    at_index = clone_url.index('@')

    # Extract the portion after '@' character
    variable1 = clone_url[at_index+1:]

    # # Extract the path (repository name) from the variable1
    # path_index = variable1.index('/')
    
    # Extract the repository path from the URL
    repository_path = clone_url.split("/")[-1]

    # Extract the username and apppassword for Bitbucket
    username = bitbucket_username
    apppassword = bitbucket_app_password

    # Create the desired URL for Bitbucket
    desired_url = f"https://{username}:{apppassword}@bitbucket.org/{workspace}/{repository_path}"
   
    print(desired_url)

    # Change to the cloned repository directory
    os.chdir(repo_dir)

    # Add the bitbucket_app_password to the bitbucket_repo_url
    bitbucket_repo_url_with_password = desired_url


    # Add Bitbucket remote
    origin = repo.create_remote("bitbucket", bitbucket_repo_url_with_password)

    # Fetch all remote branches
    repo.remotes.origin.fetch()

    # Push all local branches to Bitbucket repository
    for branch in repo.branches:
        branch_name = str(branch)
        origin.push(refspec=f"refs/heads/{branch_name}:refs/heads/{branch_name}")

    # Push all tags to Bitbucket repository (normal push)
    repo.git.push("bitbucket", "--tags")

    # Clean up the repository directory
    os.chdir("..")
    shutil.rmtree(repo_dir)



@app.route('/export', methods=['POST'])
def importFromGitlab():
    data = request.get_json()
    # print(data)
    try:
        import env
        # GitLab API endpoint and access token
        # gitlab_api_url = env.gitlab_api_url
        # gitlab_token = env.gitlab_token

        gitlab_api_url = data['input_gitlab_api_url']
        gitlab_token = data['input_gitlab_token']
    except [ImportError, AttributeError]:
        return ("Please enter valid credentials.")
    
    # Clean up the temporary repository directory before starting
    cleanup_temp_repo()

    #Import all the repositories from GitLab
    importedData = fetch_gitlab_groups_and_projects(gitlab_token, gitlab_api_url)

    
    return jsonify(importedData)

@app.route('/import' , methods=['POST'])
def exportToBitbucket():
    data = request.get_json()
    # print(data)

    bitbucket_username = data['input_bitbucket_username']
    bitbucket_app_password = data['input_bitbucket_app_password']
    bitbucket_api_url = data['input_bitbucket_api_url']
    workspace = data['input_workspace']
    importedData = data['input_importedData']
    

    for eachRepo in importedData:
        # print(eachRepo)
        group_name, project_name, clone_url = eachRepo

        create_bitbucket_project(group_name , bitbucket_username , bitbucket_app_password , bitbucket_api_url , workspace)
        create_bitbucket_repository(group_name, project_name, clone_url ,  bitbucket_username , bitbucket_app_password, bitbucket_api_url , workspace)


    return ("export successful")

if __name__ == '__main__':
    app.run()