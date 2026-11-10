import re

with open('docs/extracted_pdf_text.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

pages_raw = raw.split('=== PAGE ')
pages_clean = {}

for p in pages_raw:
    if not p.strip(): continue
    p_num = p.split(' ===')[0].strip()
    body = p.split(' ===\n')[1]
    
    words = [w.strip() for w in body.split('\n') if w.strip()]
    text = ' '.join(words)
    text = re.sub(r'\s+', ' ', text)
    pages_clean[p_num] = text

with open('docs/reconstructed_pages.txt', 'w', encoding='utf-8') as f:
    for p_num, content in pages_clean.items():
        f.write(f"\n==================== PAGE {p_num} ====================\n")
        f.write(content + "\n")

print("Reconstructed successfully!")
