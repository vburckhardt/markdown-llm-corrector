# Markdown LLM Corrector

This tool processes markdown files, correcting errors and inconsistencies using Large Language Model (LLM).

While still undergoing refinement, the tool produces relatively 'usable' results, as demonstrated in the samples section below.

## LLM Model

The current version leverages the LLAMA 2-70B chat model through IBM WatsonX.
The tool is built using [Langchain](https://python.langchain.com/docs/get_started/introduction). The design based on Langchain makes it easy to target other LLMs in the future.

## Samples

Some samples of original markdown files and their automated correction are available under the [samples](./samples/) directory.

## Usage

### Prerequisites

Ensure you have valid IBM Cloud API key and WatsonX project ID set as environment variables.

- Set IBM_CLOUD_API_KEY: Your [IBM Cloud API Key](https://cloud.ibm.com/docs/account?topic=account-userapikey&interface=ui#create_user_key).
- Set PROJECT_ID: Your Watson Machine Learning [Project ID](https://dataplatform.cloud.ibm.com/docs/content/wsj/analyze-data/fm-project-id.html?context=wx).

Ensure you have [markdownlint](https://www.npmjs.com/package/markdownlint) installed on the machine running this tool. Prior to passing the content to the LLM, the markdown structure is corrected using markdownlint.

### Clone the Repo

Clone the `markdown-llm-corrector` repo locally. In a terminal, run:

```bash
git clone https://github.com/vburckhardt/markdown-llm-corrector.git
```

### Install Python Dependencies

To install, run the following command:

```
pip install -r ./requirements.txt
```

### Usage

To use the tool, run the following command:

#### Run with a Single Markdown File

```bash
python main.py --input_file path/to/your/markdown_file.md
```

#### Run with a Directory of Markdown Files

```bash
python main.py --input_dir path/to/directory/containing/markdown_files
```

#### GitHub Repository

You can specify a GitHub repository using the `--repo_org` and `--repo_name` flags:

- --repo_org: Specify the GitHub organization of the repository.
- --repo_name: Specify the name of the GitHub repository.

The tool opens a PR with the corrected MD files.

```bash
python main.py --repo_org ORG_NAME --repo_name REPO_NAME
```

### Options

- `--repo_org`: Specify the GitHub organization of the repository.
- `--repo_name`: Specify the GitHub repository name.
- `--input_file`: Provide a path to a single input markdown file.
- `--input_dir`: Provide a path to a directory containing markdown files.
- `--working_dir`: Set a working directory for operations. Defaults to a randomly generated directory name.

### Description

This tool leverages IBM Watson's LLM model to correct Markdown files. It can be utilized to correct a single file or a directory of files. If run on a GitHub repository, it can also create a pull request with the corrected files.

### Contributing

Contributions are welcome! Please open a pull request with your proposed changes.

### License

This project is licensed under the Apache 2 License.
