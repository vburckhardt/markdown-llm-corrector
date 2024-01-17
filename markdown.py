import re
import textwrap
import logging

from concurrent.futures import ThreadPoolExecutor
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import MarkdownTextSplitter
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain_community.document_loaders import DirectoryLoader


class MarkdownEditor:
    def __init__(
        self,
        example_selector,
        llm_model,
        input_dir,
        original_file_path,
        replace_with_correction=False,
        verbose=True,
        corrected_file_name_suffix="_corrected",
    ):
        self.example_selector = example_selector
        self.llm_model = llm_model
        self.input_dir = input_dir
        self.original_file_path = original_file_path
        self.replace_with_correction = replace_with_correction
        self.verbose = verbose
        self.corrected_file_name_suffix = corrected_file_name_suffix

    def process_markdown(self):
        if self.original_file_path is not None:
            loader = TextLoader(self.original_file_path)
        else:
            loader = DirectoryLoader(
                self.input_dir,
                glob="**/*.md",
                show_progress=False,
                loader_cls=TextLoader,
            )

        data = loader.load()

        for doc in data:
            doc.page_content = self.__remove_code_tables_comments(doc.page_content)

        text_splitter = MarkdownTextSplitter(chunk_size=600, chunk_overlap=0)

        data = text_splitter.transform_documents(data)

        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self.__process_chunk, doc) for doc in data]
            results = [future.result() for future in futures]

        # Reduce results
        corrections_by_file = {}
        for result in results:
            if result[2].metadata["source"] not in corrections_by_file:
                corrections_by_file[result[2].metadata["source"]] = []
            corrections_by_file[result[2].metadata["source"]].append(result[0:2])

        for original_file_path, corrections in corrections_by_file.items():
            with open(original_file_path, "r") as file:
                modified_contents = file.read()

            for original, correction in corrections:
                # Strip newlines from original and correction
                original_stripped = original.strip("\n")
                correction_stripped = correction.strip("\n")

                if original in modified_contents:
                    modified_contents = modified_contents.replace(
                        original, correction_stripped
                    )
                else:
                    # Log or handle cases where the original is not found
                    logging.info("'%s' not found in the document.", original_stripped)

            if self.replace_with_correction:
                new_file_path = original_file_path  # Override file content in git mode
            else:
                new_file_path = (
                    original_file_path.rsplit(".", 1)[0]
                    + self.corrected_file_name_suffix
                    + ".md"
                )

            with open(new_file_path, "w") as file:
                file.write(modified_contents)

    def __process_chunk(self, chunk):
        original = chunk.page_content
        example_prompt = PromptTemplate(
            input_variables=["text", "correction"],
            template=textwrap.dedent(
                """\
                [[[Text]]]
                {text}

                [[[Correction]]]
                {correction}</end>"""
            ),
        )

        examples_selected = self.example_selector.select_examples({"text": original})

        prompt = FewShotPromptTemplate(
            examples=examples_selected,
            # example_selector=
            example_prompt=example_prompt,
            prefix=textwrap.dedent(
                """\
                [[[Instruction]]]
                You are an advanced AI text editor tasked with enhancing the clarity, accuracy, and readability of markdown text. Your primary function is to meticulously identify and correct any errors in spelling, grammar, and wording. Additionally, ensure the consistency of the text while diligently preserving the original markdown formatting. Respond exclusively with the refined text, maintaining the essence and structure of the original content."""
            ),
            suffix=textwrap.dedent(
                """\
                [[[Text]]]
                {text}

                [[[Correction]]]
                """
            ),
            input_variables=["text"],
        )

        chain = LLMChain(llm=self.llm_model, prompt=prompt, verbose=self.verbose)
        correction = chain(original)["text"].split("</end>")[0]
        return original, correction, chunk

    def __remove_code_tables_comments(self, markdown_text):
        # Remove code blocks
        no_code = re.sub(r"```.*?```", "", markdown_text, flags=re.DOTALL)

        # Remove tables
        no_tables = re.sub(
            r"\|.*?\n\|[-| :]*\|.*?\n(\|.*?\n)*", "", no_code, flags=re.DOTALL
        )

        # Some tables do not have | for first column
        no_tables = re.sub(
            r"\n.*?\n[-| :]*\|.*?\n(.*?\n)*", "\n", no_tables, flags=re.DOTALL
        )

        # Remove HTML-style comments
        no_comments = re.sub(r"<!--.*?-->", "", no_tables, flags=re.DOTALL)

        return no_comments
