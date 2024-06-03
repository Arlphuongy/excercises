import pandas as pd

def parse_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    parsed_data = []
    for line in lines:
        parts = line.split(' ')
        lines_processed = int(parts[1])
        file_name = parts[-1].strip()
        parsed_data.append([lines_processed, file_name])
    
    return pd.DataFrame(parsed_data, columns=['lines', 'file'])

file_path_1 = 'dataset.txt'  
file_path_2 = 'dataset_t.txt'  

dataset_1 = parse_lines(file_path_1)
dataset_2 = parse_lines(file_path_2)

merged_dataset = dataset_1.merge(dataset_2, on='file', suffixes=('_dataset_1', '_dataset_2'))

mismatched_lines = merged_dataset[merged_dataset['lines_dataset_1'] != merged_dataset['lines_dataset_2']]

if mismatched_lines.empty:
    print("No mismatched lines found.")
else:
    print("Mismatched lines:")
    print(mismatched_lines)
