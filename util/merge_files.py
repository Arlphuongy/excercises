import glob
import nltk
import jieba
import json

def write_lines(pairs_path, ori_file, tran_file, counter):
    with open(ori_file, 'r', encoding='utf-8') as f1:
        ori_lines = [line.strip() for line in f1.readlines()]

    with open(tran_file, 'r', encoding='utf-8') as f2:
        tran_lines = [line.strip() for line in f2.readlines()]

    if len(ori_lines) == len(tran_lines):
        pass
    else:
        # something to delete sentences that aren't translation pairs
        print("the number of lines in the files don't match.")

    

    # ori_words = []
    # tran_words = []

    # for line in ori_lines:
    #     ori_words.extend(nltk.word_tokenize(line))

    # for line in tran_lines:
    #     tran_words.extend(jieba.cut(line, cut_all=False))

    # unique_words_ori = len(set(ori_words))
    # print(f"Number of unique words in ori_lines: {unique_words_ori}")

    # unique_words_tran = len(set(tran_words))
    # print(f"Number of unique words in tran_lines: {unique_words_tran}")


    train_lines = int(0.8 * len(ori_lines))

    with open(f"{pairs_path}train_{counter}.json", "w", encoding='utf-8') as train_file:
        data = []
        for i in range(train_lines):
            # ori_line = ori_lines[i]
            # tran_line = tran_lines[i]
            # if 15 < len(ori_line) < 512 and 15 < len(tran_line) < 512:
            #     data.append({
            #         "translation": {
            #             "en": ori_line,
            #             "zh": tran_line
            #         }
            #     })
            data.append({
                "translation": {
                    "en": ori_lines[i],
                    "vi": tran_lines[i]
                }
            })

        json_object = json.dumps(data, indent=4, ensure_ascii=False)
        train_file.write(json_object)

    with open(f"{pairs_path}validation_{counter}.json", "w", encoding='utf-8') as validation_file:
        data = []
        for i in range(train_lines, len(ori_lines)):
            # ori_line = ori_lines[i]
            # tran_line = tran_lines[i]
            # if 15 < len(ori_line) < 512 and 15 < len(tran_line) < 512:
            #     data.append({
            #         "translation": {
            #             "en": ori_line,
            #             "zh": tran_line
            #         }
            #     })
            data.append({
                "translation": {
                    "en": ori_lines[i],
                    "vi": tran_lines[i]
                }
            })

        json_object = json.dumps(data, indent=4, ensure_ascii=False)
        validation_file.write(json_object)


def get_numeric_part(filename):
    return int(''.join(filter(str.isdigit, filename)))


def get_subtitle_files(sub_path, pairs_path):
    en_pattern = f'{sub_path}en_*.txt'
    vn_pattern = f'{sub_path}vn_*.txt'

    en_files = sorted(glob.glob(en_pattern), key=get_numeric_part)
    vn_files = sorted(glob.glob(vn_pattern), key=get_numeric_part)

    i = 0
    for en_file, vn_file in zip(en_files, vn_files):
        i += 1
        write_lines(pairs_path, en_file, vn_file, i)


def main():
    # pairs_path = 'ex_4/files/zlib_trans_pairs/'
    # en_file = 'src/temp/dataset_sentence_ori.txt'
    # zh_file = 'src/temp/dataset_sentence_tran.txt'

    sub_path = 'ex_4/vn-en-netflix/subtitles_vn_en/'
    pairs_path = 'ex_4/vn-en-netflix/netflix_vn_en/'
    get_subtitle_files(sub_path, pairs_path)
    
    # write_lines(pairs_path, en_file, zh_file, 24)

main()
