import json
import glob

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

    train_lines = int(0.8 * len(ori_lines))
    with open(f"{pairs_path}train_{counter}.json", "w", encoding='utf-8') as train_file:
        data = []
        for i in range(train_lines):
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
    zh_pattern = f'{sub_path}zh_*.txt'

    en_files = sorted(glob.glob(en_pattern), key=get_numeric_part)
    zh_files = sorted(glob.glob(zh_pattern), key=get_numeric_part)

    # print(en_files)
    # print(zh_files)

    i = 0
    for en_file, zh_file in zip(en_files, zh_files):
        i += 1
        write_lines(pairs_path, en_file, zh_file, i)


def main():
    sub_path = 'ex_4/files/subtitles/'
    pairs_path = 'ex_4/files/trans_pairs/'

    get_subtitle_files(sub_path, pairs_path)

main()







    # if is_train:
    #     output_file = f"{pairs_path}train_{i}.json"
    # else:
    #     count = getattr(write_lines, 'count' , 1)
    #     output_file = f"{pairs_path}validation_{count}.json"
    #     setattr(write_lines, 'count', count + 1)


    # with open(output_file, "w", encoding='utf-8') as file:
    #     data = []
    #     for i in range(len(ori_lines)):
    #         data.append({
    #             "translation": {
    #                 "en": ori_lines[i],
    #                 "vi": tran_lines[i]
    #             }
    #         })

    #     json_object = json.dumps(data, indent=4, ensure_ascii=False)
    #     file.write(json_object + "\n")