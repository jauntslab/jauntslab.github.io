import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import re
import json

def parse_author_names(raw_authors):
    names = [name.strip() for name in raw_authors.split(" and ")]
    formatted = []
    for name in names:
        if "," in name:
            last, first = [part.strip() for part in name.split(",", 1)]
            formatted.append(f"{first} {last}")
        else:
            formatted.append(name)
    return ", ".join(formatted)

def bib_entry_to_json(entry):
    return {
        "title": entry.get("title", "").replace("{", "").replace("}", ""),
        "authors": parse_author_names(entry.get("author", "")),
        "venue": entry.get("booktitle", entry.get("journal", "")),
        "year": entry.get("year", ""),
        "link": entry.get("arxiv_url", entry.get("doi_url", entry.get("pdf_url", entry.get("url", "")))),
        "github": entry.get("code_url", ""),
        "poster": entry.get("poster_url", ""),
        "slides": entry.get("slides_url", ""),
        "project": entry.get("project_url", "")
    }

def load_bibtex_to_json(input_file, output_file):
    with open(input_file, encoding="utf-8") as bibtex_file:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

    json_entries = [bib_entry_to_json(entry) for entry in bib_database.entries]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_entries, f, indent=2, ensure_ascii=False)

# 실행 예시
load_bibtex_to_json("pujara_pubs.bib", "publication.json")
