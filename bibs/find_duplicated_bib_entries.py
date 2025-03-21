import os
import bibtexparser
import re
from collections import defaultdict

# this scripts extracts the duplicated bib keys in several bib files
# it reads all the bib entries (key+title), normalize the title and append the key to the map (title, keys[])
def normalize_title(title):
    """
    Normalize the title by:
    1. Removing braces '{}' but preserving the content inside them.
    2. Stripping spaces and converting to lowercase.
    3. Removing some punctuation (optional, depending on the desired strictness).
    """
    # Remove braces while keeping content inside them
    title = re.sub(r'[{}]', '', title)
    # Strip leading/trailing spaces and convert to lowercase
    title = title.strip().lower()
    # Optional: Remove other punctuation like periods, commas, quotes, etc.
    title = re.sub(r'[():.,\'"!?]', '', title)
    return title

def parse_bib_files(directory):
    # Dictionary to map titles to a list of keys
    title_to_keys = defaultdict(list)
    
    # Traverse the directory and process each .bib file
    for filename in os.listdir(directory):
        if filename.endswith(".bib"):
            print('Parsing: ', filename)
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as bib_file:
                try:
                    # Parse the bib file using bibtexparser
                    bib_database = bibtexparser.load(bib_file)
                    for entry in bib_database.entries:
                        key = entry.get('ID')  # Get the bib entry key
                        title = entry.get('title')  # Get the bib entry title
                        if title and key:
                            # Normalize the title (removing braces, lowercasing, etc.)
                            normalized_title = normalize_title(title)
                            title_to_keys[normalized_title].append(key)
                except Exception as e:
                    print(f"Error parsing {file_path}: {e}")

    return title_to_keys

def write_duplicates_to_file(title_to_keys, output_file):
    """Write titles with multiple keys to a file."""
    with open(output_file, 'w', encoding='utf-8') as file:
        for title, keys in title_to_keys.items():
            if len(keys) > 1:
                file.write(f"Title: '{title}' has multiple keys: {keys}\n")
        print(f"Duplicate entries have been written to {output_file}")

# Example usage:
if __name__ == "__main__":
    directory = "bibs"  # Update this path
    output_file = "bibs/duplicate_titles.txt"  # Define the output file path
    title_to_keys_map = parse_bib_files(directory)
    
    # Write duplicates to file
    write_duplicates_to_file(title_to_keys_map, output_file)