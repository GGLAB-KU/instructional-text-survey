import os
import re
from collections import defaultdict
import bibtexparser

# this script extracts all the references from latex, extract their titles from provided bib files
# dump them to a file, and identify the references that has mutliple bib keys

def normalize_title(title):
    # Remove curly braces, extra whitespace, and make lowercase
    return re.sub(r'[{}]', '', title).strip().lower()

def extract_citation_keys(latex_dir):
    citation_keys = set()
    citation_pattern = re.compile(r"\\cite[t|p]?(\[.*?\])?\{(.*?)\}")

    for root, dirs, files in os.walk(latex_dir):
        for file in files:
            if file.endswith(".tex"):
                print(f"Processing tex file {file}" )
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    matches = citation_pattern.findall(content)
                    for match in matches:
                        keys = match[1].split(',')
                        for key in keys:
                            citation_keys.add(key.strip())
    return citation_keys

def parse_bib_files(bib_dir, citation_keys):
    title_to_keys = defaultdict(list)
    for filename in os.listdir(bib_dir):
        if filename.endswith(".bib"):
            print(f"Processing {filename}")
            file_path = os.path.join(bib_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as bib_file:
                try:
                    bib_database = bibtexparser.load(bib_file)
                    for entry in bib_database.entries:
                        key = entry.get('ID')
                        title = entry.get('title')
                        if key in citation_keys and title:
                            normalized_title = normalize_title(title)
                            title_to_keys[normalized_title].append(key)
                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")
    return title_to_keys

def find_duplicate_titles(title_to_keys):
    return {title: keys for title, keys in title_to_keys.items() if len(keys) > 1}

def save_results(key_to_title, output_file, duplicates_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for title, keys in key_to_title.items():
            if len(keys) > 1:
                with open(duplicates_file, 'w', encoding='utf-8') as dup_file:
                    dup_file.write(f"{title} | {','.join(keys)}\n")
            
            file.write(f"{title} | {','.join(keys)}\n")

# Example usage
latex_directory = 'sections'  # Change this to the path of your LaTeX files directory
bib_directory = 'bibs'  # Change this to the path of your BibTeX files directory
output_file_path = 'output_keys_and_titles.txt'  # Output file path
duplicates_file_path = 'duplicates_titles.txt'  # File for duplicates

citation_keys = extract_citation_keys(latex_directory)
title_to_keys = parse_bib_files(bib_directory, citation_keys)
duplicates = find_duplicate_titles(title_to_keys)
save_results(title_to_keys, output_file_path, duplicates_file_path)

print(f"Results saved to {output_file_path}")
print(f"Duplicates saved to {duplicates_file_path}")
