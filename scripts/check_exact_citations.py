import re

with open('docs/extracted_pdf_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize spacing
lines = [l.strip() for l in text.split('\n') if l.strip()]
clean_text = ' '.join(lines)
clean_text = re.sub(r'\s+', ' ', clean_text)

dp_pos = clean_text.find('DAFTAR PUSTAKA')
body_text = clean_text[:dp_pos]

bracket_citations = re.findall(r'\[\d+\]', body_text)
print("Bracket citations found in body text:", set(bracket_citations))
for c in sorted(set(bracket_citations)):
    matches = [m.start() for m in re.finditer(re.escape(c), body_text)]
    print(f"Citation {c}: {len(matches)} times")
    for idx in matches:
        snippet = body_text[max(0, idx-50):min(len(body_text), idx+50)]
        print(f"   ...{snippet}...")

# Also check for author-year citations
author_year = re.findall(r'[A-Z][a-zA-Z\s&]+\(\d{4}\)', body_text)
print("\nAuthor-year citations found:", set(author_year))

