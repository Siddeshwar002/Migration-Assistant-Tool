## Disclaimer
This tool was NOT written by Atlassian developers and is considered a third-party tool. This means that this is also NOT supported by Atlassian. We highly recommend you have your team review the script before running it to ensure you understand the steps and actions taking place, as Atlassian is not responsible for the resulting configuration.

## Purpose
This script allows you to migrate GitLab repositories to Bitbucket Cloud. It provides functionality to export GitLab groups and projects to a CSV file and then create corresponding projects and repositories in Bitbucket Cloud. The migration process involves cloning GitLab repositories and pushing them to Bitbucket repositories.

## How to Use

Configure a python virtual environment and install package dependencies with the follow commands:

        python3 -m venv venv
        source venv/Scripts/activate  # If using gitbash on Windows
        source venv/bin/activate      # If on linux/mac
        pip3 install -r requirements.txt

Once the dependencies are satisfied and you have provided your unique details, simply run the script with Python 3.6+ and follow any prompts.

Run script with python via:

        python3 migration.py export #To export GitLab groups and projects to a CSV file.

        python3 migration.py repo-push #To create corresponding Bitbucket projects and repositories from the exported CSV file.
        
## Note
If your repository contains LFS files or if its size exceeds 4 GB, please exclude those repositories from the gitlab_projects.csv file. For such cases, it is recommended to perform a manual migration using the git mirror clone command.
