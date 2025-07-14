from jinja2 import Template
from worldbuilder.paths import prompt_file

def load_prompt(name: str, variables: dict = {}) -> str:
    path = prompt_file(name)
    raw = path.read_text(encoding="utf-8")
    return Template(raw).render(**variables)