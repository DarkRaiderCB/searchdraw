import os
import re
from html import unescape
import argparse


def extract_full_text_from_drawio(file_path):
    """Reads and normalizes all string-like content in a .drawio file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw = f.read()
            decoded = unescape(raw.lower())
            return decoded
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
        return ""


def search_drawio_files(root_dir, query):
    query_words = re.findall(r'\w+', query.lower())
    matching_files = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".drawio"):
                file_path = os.path.join(dirpath, filename)
                full_text = extract_full_text_from_drawio(file_path)

                if all(word in full_text for word in query_words):
                    matching_files.append(file_path)

    return matching_files


def main():
    parser = argparse.ArgumentParser(
        prog="searchdraw",
        description="Search .drawio files for a query.")
    parser.add_argument("--dir", default=".", help="Directory to search in")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--version", action="version",
                        version="1.0")
    args = parser.parse_args()

    results = search_drawio_files(args.dir, args.query)

    if results:
        print("\nMatching .drawio files:")
        for path in results:
            print(path)
    else:
        print("No matching .drawio files found.")
