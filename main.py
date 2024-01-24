import argparse
import logging

from data import examples
from utils import Utils
from git import Git
from markdown import MarkdownEditor

from ibm_watson_machine_learning.foundation_models.utils.enums import (
    ModelTypes,
    DecodingMethods,
)
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.extensions.langchain import (
    WatsonxLLM,
)
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector

logging.basicConfig(level=logging.WARN)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process markdown files for corrections."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--repo_org", help="Specify the GitHub organization of the repository."
    )
    group.add_argument(
        "--input_file", help="Provide a path to a single input markdown file."
    )
    group.add_argument(
        "--input_dir", help="Provide a path to a directory containing markdown files."
    )

    parser.add_argument("--repo_name", help="Specify the GitHub repository name.")

    args = parser.parse_args()
    if args.repo_org and not args.repo_name:
        parser.error("--repo_name is required when --repo_org is specified.")

    parser.add_argument(
        "--working_dir",
        default=f"./.{Utils.generate_random_name(20)}",
        help="Set a working directory for operations. Defaults to a randomly generated directory name.",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    original_file_path = args.input_file
    input_dir = args.input_dir
    repo_owner = args.repo_org
    repo_name = args.repo_name
    working_dir = args.working_dir

    is_running_on_git_clone = repo_name is not None

    apikey = Utils.get_env_variable(
        "IBM_CLOUD_API_KEY", "Please enter your WML api key (hit enter): "
    )
    project_id = Utils.get_env_variable(
        "PROJECT_ID", "Please enter your project_id (hit enter): "
    )

    if is_running_on_git_clone:
        git = Git(repo_owner, repo_name, working_dir)
        git.clone()
        input_dir = f"{working_dir}/{repo_name}"

    credentials = {"url": "https://us-south.ml.cloud.ibm.com", "apikey": apikey}
    parameters = {
        GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
        GenParams.STOP_SEQUENCES: ["</end>", "Text:<startoftext>"],
        GenParams.MAX_NEW_TOKENS: 1500,
        GenParams.MIN_NEW_TOKENS: 1,
    }

    model = Model(
        model_id=ModelTypes.LLAMA_2_70B_CHAT,
        params=parameters,
        credentials=credentials,
        project_id=project_id,
    )

    model_llm = WatsonxLLM(model=model)

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        HuggingFaceEmbeddings(),
        FAISS,
        k=10,
    )

    markdown_editor = MarkdownEditor(
        example_selector,
        model_llm,
        input_dir,
        original_file_path,
        replace_with_correction=is_running_on_git_clone,
        verbose=False
    )

    markdown_editor.process_markdown()

    if is_running_on_git_clone:
        git.create_pull_request()


if __name__ == "__main__":
    main()
