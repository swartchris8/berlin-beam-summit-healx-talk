from spacy import displacy
import spacy
from pathlib import Path
import re

colors = {"DRUG": "hsla(100, 30%, 50%, 0.9)", "DISEASE": "salmon"}
options = {"ents": ["DRUG", "DISEASE"], "colors": colors, "font": "Source Sans Pro", "bg": "#F3F3F3", "collapse_phrases": True}

output_path = Path("talk/talk3.html")


def make_entity_dict(keyword, label, text):
    entities_dict = [
        {"start": m.start(), "end": m.start() + len(keyword), "label": label}
        for m in re.finditer(keyword, text)
    ]
    print(entities_dict)
    return entities_dict


text = """Aspirin treats headaches.
Aspirin can help prevent heart attacks."""
entity_dicts = make_entity_dict("Aspirin", "DRUG", text) + make_entity_dict("headaches", "DISEASE", text) + make_entity_dict("heart attacks", "DISEASE", text)
sorted_entity_dicts = sorted(entity_dicts, key=lambda k: k['start'])

ex = [{"text": text,
       "ents": sorted_entity_dicts,
       "title": None}]
html = displacy.render(ex, style="ent", manual=True, options=options)
output_path.open("w", encoding="utf-8").write(html)

nlp = spacy.load('en_core_web_lg')
doc = nlp(unicode(text))
svg = displacy.render(doc, style="dep")
output_path = Path("talk/dep.svg")
output_path.open("w", encoding="utf-8").write(svg)


# ex = [{"text": "Aspirin treats headaches. Aspirin can help prevent heart attacks.",
#        "ents": [{"start": 0, "end": 7, "label": "DRUG"},
#                 {"start": 15, "end": 24, "label": "DISEASE"},
#                 {"start": 26, "end": 33, "label": "DRUG"}],
#        "title": None}]
# html = displacy.render(ex, style="ent", manual=True)
