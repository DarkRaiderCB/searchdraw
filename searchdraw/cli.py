import os
import re
import sys
from html import unescape
import argparse
from xml.etree import ElementTree as ET


def extract_visible_text_from_drawio(file_path, case_sensitive=False):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_xml = f.read()

        tree = ET.fromstring(raw_xml)
        text_blobs = []

        for cell in tree.iter("mxCell"):
            value = cell.attrib.get("value", "")
            if value:
                unescaped = unescape(value)
                # Remove HTML tags
                # cleaned = re.sub(r'<[^>]+>', '', unescaped)
                cleaned = unescaped
                normalized = cleaned.strip()
                if not case_sensitive:
                    normalized = normalized.lower()
                if normalized:
                    text_blobs.append(normalized)

        return " ".join(text_blobs)

    except Exception as e:
        print(f"Could not parse {file_path}: {e}")
        return ""


def search_drawio_files(root_dir, query, case_sensitive=False):
    if not case_sensitive:
        query = query.lower()
    query_words = re.findall(r'\w+', query.lower())
    matching_files = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".drawio"):
                file_path = os.path.join(dirpath, filename)
                full_text = extract_visible_text_from_drawio(file_path)

                if all(word in full_text for word in query_words):
                    matching_files.append(file_path)

    return matching_files


def main():
    parser = argparse.ArgumentParser(
        prog="searchdraw",
        description="Search .drawio files for a query.")
    parser.add_argument("query", help="Search query string (quoted if multiple words)")
    parser.add_argument("path", help="Path to directory containing .drawio files")
    parser.add_argument("-C", "--case-sensitive", action="store_true",
                        help="Enable case-sensitive matching")
    parser.add_argument("--version", action="version",
                        version="2.0")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a valid directory.")
        sys.exit(1)

    results = search_drawio_files(args.path, args.query, args.case_sensitive)

    if results:
        print("\nMatching .drawio files:")
        for path in results:
            print(path)
    else:
        print("No matching .drawio files found.")
