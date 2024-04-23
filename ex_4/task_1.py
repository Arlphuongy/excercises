import json

def write_lines(ori_file, tran_file):
    with open(ori_file, 'r', encoding='utf-8') as f1:
        ori_lines = [line.strip() for line in f1.readlines()]

    with open(tran_file, 'r', encoding='utf-8') as f2:
        tran_lines = [line.strip() for line in f2.readlines()]

    if len(ori_lines) == len(tran_lines):
        pass
    else:
        # something to delete sentences that aren't translation pairs
        print("the number of lines in the files don't match.")

    with open("ex_4/sentences.json", "w", encoding='utf-8') as file:
        data = []
        for i in range(len(ori_lines)):
            data.append({
                "translation": {
                    "en": ori_lines[i],
                    "vi": tran_lines[i]
                }
            })

        json_object = json.dumps(data, indent=4, ensure_ascii=False)
        file.write(json_object)


write_lines('src/temp/dataset_sentence_ori.txt', 'src/temp/dataset_sentence_tran.txt')


    










    
# print(checklines(ori_file, tran_file))