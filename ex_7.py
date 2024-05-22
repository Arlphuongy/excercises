import torch
import time
import re
import sys

from transformers import MarianTokenizer, MarianMTModel, AutoTokenizer
from ctranslate2 import Translator
from transformers import AutoTokenizer
from hf_hub_ctranslate2 import TranslatorCT2fromHfHub, GeneratorCT2fromHfHub


def print_source_texts(src_texts):
    print("Source Texts:\n")
    for idx, text in enumerate(src_texts, 1):
        print(f"{idx}. {text}")
    print("\n" + "=" * 80 + "\n")


def print_translations(
    model_dir,
    src_lang,
    tgt_lang,
    src_texts,
    translations,
    translation_time,
    log_file_name,
):
    with open(log_file_name, "w", encoding="utf-8") as log_file:
        print(f"Model: {model_dir}", file=log_file)

        # Determine the maximum number of digits in the largest index
        max_index_length = len(str(len(src_texts)))

        for idx, (src, trans) in enumerate(zip(src_texts, translations), 1):
            # Convert index to string and left-justify it within the space determined by max_index_length
            # This ensures the index + '.' takes up the same amount of space for each entry
            index_str = f"{idx}.".ljust(max_index_length + 2)

            print(
                f"{index_str} <{src_lang}> {src}\n{' ' * (max_index_length + 2)} <{tgt_lang}> {trans}\n",
                file=log_file,
            )
            # print(trans, file=log_file)

        print(f"Translation time: {translation_time:.3f}s", file=log_file)
        print("=" * 80, file=log_file)
        print(file=log_file)


def translate_with_ct2fast_model(texts, src_lang, tgt_lang, model_dir, log_file_name):
    torch.cuda.reset_peak_memory_stats()
    torch.cuda.synchronize()

    model = TranslatorCT2fromHfHub(
        model_name_or_path=model_dir,
        device="cuda",
        compute_type="int8_float16",
        tokenizer=AutoTokenizer.from_pretrained(model_dir),
    )

    start_time = time.time()
    outputs = model.generate(text=texts)
    end_time = time.time()

    translations = [output for output in outputs]
    translation_time = end_time - start_time
    print_translations(
        model_dir,
        src_lang,
        tgt_lang,
        texts,
        translations,
        translation_time,
        log_file_name,
    )


def translate_with_opus_mt(texts, src_lang, tgt_lang, model_name, log_file_name):
    # Ensure all CUDA operations have finished
    torch.cuda.synchronize()

    # Load the tokenizer and model
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name).to("cuda")

    # Translate texts
    start_time = time.time()

    batch_size = 512  # You can adjust this based on your GPU memory
    translated_texts = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]

        # Tokenize the batch
        tokenized_batch = tokenizer(
            batch, return_tensors="pt", padding=True, truncation=True, max_length=256
        ).to("cuda")

        # Translate the tokenized batch
        with torch.no_grad():
            translated = model.generate(**tokenized_batch)

        # Decode the translated tokens
        translated_texts.extend(
            [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
        )

    end_time = time.time()

    # Instead of printing directly inside the function:
    translations = [translation for translation in translated_texts]
    translation_time = end_time - start_time

    # Use the new print function
    print_translations(
        model_name,
        src_lang,
        tgt_lang,
        texts,
        translations,
        translation_time,
        log_file_name,
    )


if __name__ == "__main__":
    src_texts = []

    # Function to read lines from a file, check each line, and append to src_texts if conditions are met
    def add_texts_from_file(file_path, target_list):
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace
                if (
                    line and len(line) > 20
                ):  # Check if line is not empty and has more than 20 characters
                    target_list.append(line)

    add_texts_from_file("src/zh_testing_content.txt", src_texts)

    translate_with_ct2fast_model(
        src_texts, "zh", "en", "weights/ct2fast-mix-zh-en-1m", ".log/zh-en-1m"
    )
    # translate_with_opus_mt(src_texts, "Eugenememe/news-en-vi")
    # translate_with_ct2fast_model(src_texts, "ct2fast-news-en-vi")
