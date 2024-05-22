import glob
import os
import re
import nltk
from docx import Document

nltk.download("punkt")
import argparse


def numerical_sort_key(s):
    # Updated pattern to match 'dataset_' followed by 1 to 3 digits
    match = re.search(r"dataset_(\d{1,3})", os.path.basename(s))

    if match:
        # Extract and return the sentence number as an integer
        return int(match.group(1))
    else:
        # Return a default value or raise an error if the pattern is not found
        return None  # or raise ValueError("Pattern not found")


def extract_lines_from_docx(docx_files, txt_path):
    total_lines = 0
    total_words = 0

    with open(txt_path, "w", encoding="utf-8") as txt_file:  # Open in append mode
        for docx_path in docx_files:
            document = Document(docx_path)
            file_lines = 0
            file_words = 0

            for paragraph in document.paragraphs:
                text = paragraph.text.strip()  # Remove leading/trailing whitespaces
                if text:  # Check if the line is not empty
                    words = nltk.word_tokenize(text)
                    txt_file.write(
                        text + "\n"
                    )  # Write to the .txt file and add a newline
                    file_lines += 1
                    file_words += len(words)

            total_lines += file_lines
            total_words += file_words
            print(
                f"Processed {file_lines} lines and {file_words} words from {docx_path}"
            )

    print(
        f"Total: Processed {total_lines} lines and {total_words} words from all files"
    )


def find_and_process_docx(folder_path, base_filename, txt_filename, translation=True):
    if translation:
        docx_pattern = f"{folder_path}/{base_filename}_*_t.docx"
    else:
        docx_pattern = f"{folder_path}/{base_filename}_*.docx"

    docx_files = glob.glob(docx_pattern)

    # Exclude translation files when looking for original files
    if not translation:
        docx_files = [f for f in docx_files if not f.endswith("_t.docx")]

    # Sort the files using the numerical_sort_key to ensure proper numerical order
    docx_files.sort(key=numerical_sort_key)

    # Path for the output .txt file
    txt_path = f"{folder_path}/{txt_filename}"

    # Extract lines from each .docx file and append to the .txt file
    extract_lines_from_docx(docx_files, txt_path)


def main():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Process .docx files for translation pairs."
    )

    # Add arguments
    parser.add_argument(
        "--folder_path",
        type=str,
        required=True,
        help="The folder path containing .docx files",
    )
    parser.add_argument(
        "--base_filename",
        type=str,
        required=True,
        help="The base filename for .docx files",
    )
    parser.add_argument(
        "--ori_lang", type=str, required=True, help="Original language code"
    )
    parser.add_argument(
        "--tran_lang", type=str, required=True, help="Translation language code"
    )
    parser.add_argument(
        "--translation",
        choices=["ori", "tran", "both"],
        default="both",
        help="Flag to process original, translation, or both files",
    )

    args = parser.parse_args()

    translation_mapping = {
        "ori": (False, f"{args.base_filename}_sentence_ori.txt"),
        "tran": (True, f"{args.base_filename}_sentence_tran.txt"),
        "both": [
            (True, f"{args.base_filename}_sentence_tran.txt"),
            (False, f"{args.base_filename}_sentence_ori.txt"),
        ],
    }

    translations_to_process = translation_mapping[args.translation]

    # If "both" is selected, translations_to_process will be a list; otherwise, it will be a tuple.
    if isinstance(translations_to_process, list):
        for translation in translations_to_process:
            find_and_process_docx(
                args.folder_path,
                args.base_filename,
                translation[1],
                translation=translation[0],
            )
    else:
        find_and_process_docx(
            args.folder_path,
            args.base_filename,
            translations_to_process[1],
            translation=translations_to_process[0],
        )


if __name__ == "__main__":
    main()
