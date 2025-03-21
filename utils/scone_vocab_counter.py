import os
import re

def read_and_process_file(file_path):
    unique_words = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            for action in parts[2::2]:  # Assuming the action descriptions are at even indices starting from 2
                words = re.findall(r'\b\w+\b', action.lower())
                #print(words)
                unique_words.update(words)
    return unique_words

def main(directory_path):
    total_vocab = set()
    for filename in os.listdir(directory_path):
        if filename.endswith('.tsv'):  # Ensure only processing TSV files
            file_path = os.path.join(directory_path, filename)
            file_vocab = read_and_process_file(file_path)
            total_vocab.update(file_vocab)
            print(f'Vocabulary size for {filename}: {len(file_vocab)}')
    
    print(f'Total combined vocabulary size: {len(total_vocab)}')

# Replace 'path_to_dataset_directory' with the path to your dataset files
main('/home/asafa/workspace/datasets/SCONE')
