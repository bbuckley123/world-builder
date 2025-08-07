import spacy
from worldbuilder.paths import WORLD_YAML
from pathlib import Path
from typing import List, Tuple

nlp = spacy.load("en_core_web_sm")
KEYWORDS_WORLD = {"world", "realm", "planet", "plane"}
KEYWORDS_CONTINENT = {"continent", "landmass", "region", "realm", "territory"}
KEYWORDS_OCEAN = {"ocean", "sea", "waters", "current", "deep"}

def extract_world_name(text: str) -> str:
    doc = nlp(text)

    for sent in doc.sents:
        for token in sent:
            if token.pos_ == "PROPN" and token.ent_type_ in {"GPE", "LOC", "ORG", ""}:
                span = token.text
                context_window = sent[max(0, token.i -5): token.i + 5].text.lower()
                if any(keyword in context_window for keyword in KEYWORDS_WORLD):
                    print(f"Spacy found this name: {span}")
                    return span
    print("SpaCy could not find a world name!")

def extract_continent_and_ocean_names(text: str) -> Tuple[List[str], List[str]]:
    doc = nlp(text)

    continents = set()
    oceans = set()

    for sent in doc.sents:
        for token in sent:
            if token.pos_ == "PROPN" and token.ent_type_ in {"GPE", "LOC", "ORG", ""}:
                span = token.text
                context_window = sent[max(0, token.i - 5): token.i + 5].text.lower()
                if any(keyword in context_window for keyword in KEYWORDS_CONTINENT):
                    continents.add(span)
                elif any(keyword in context_window for keyword in KEYWORDS_OCEAN):
                    oceans.add(span)

    return sorted(continents), sorted(oceans)

def main():
    description_path = Path(WORLD_YAML)
    if not description_path.exists():
        raise FileNotFoundError(f"{description_path} not found")

    import yaml
    world = yaml.safe_load(description_path.read_text(encoding="utf-8"))
    text = world["description"]

    continents, oceans = extract_continent_and_ocean_names(text)

    print("🌍 Continents:")
    for name in continents:
        print(f"  - {name}")

    print("\n🌊 Oceans:")
    for name in oceans:
        print(f"  - {name}")

if __name__ == "__main__":
    main()
