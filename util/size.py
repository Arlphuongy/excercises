import datasets

dataset = datasets.load_dataset('arlzphuong/mix-zh-en-4m')

train_size = len(dataset['train'])
test_size = len(dataset['validation'])

print(f"Train set size: {train_size} examples")
print(f"Validation set size: {test_size} examples")

