import os
import requests
from utils import Utils


class Git:
    def __init__(
        self, repo_owner, repo_name, working_dir=f"./.{Utils.generate_random_name(20)}"
    ):
        self.working_dir = working_dir
        self.repo_name = repo_name
        self.repo_owner = repo_owner
        self.branch_name = f"edit-{Utils.generate_random_name()}"
        self.working_dir = working_dir
        self.github_token = Utils.get_env_variable(
            "GITHUB_TOKEN", "Please enter your github token (hit enter): "
        )

    def clone(self):
        os.system(
            f"git clone https://github.com/{self.repo_owner}/{self.repo_name}.git {self.working_dir}/{self.repo_name}"
        )

    def create_pull_request(self):
        os.chdir(f"{self.working_dir}/{self.repo_name}")
        os.system(f"git checkout -b {self.branch_name}")
        os.system("git add .")
        os.system('git commit -m "Edit markdown documents"')
        os.system(f"git push --set-upstream origin {self.branch_name}")

        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        data = {
            "title": "Update markdown documents",
            "head": self.branch_name,
            "base": "main",
            "body": """**LLM-Assisted Editing Enhancement**

To make the most of your modifications or further developments, it's advisable to use the specific branch from which this Pull Request (PR) originates. This will ensure you have a solid and up-to-date foundation for your tweaks and enhancements.

_Using [Markdown LLM Corrector](https://github.com/vburckhardt/markdown-llm-corrector)._
""",
        }
        response = requests.post(
            f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/pulls",
            headers=headers,
            json=data,
        )

        return response