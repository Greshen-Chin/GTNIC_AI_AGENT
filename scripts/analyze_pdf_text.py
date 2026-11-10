import re

with open('docs/extracted_pdf_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize spacing
lines = [l.strip() for l in text.split('\n') if l.strip()]
clean_text = ' '.join(lines)
clean_text = re.sub(r'\s+', ' ', clean_text)

print(f"Total length of clean text: {len(clean_text)} chars, {len(clean_text.split())} words")

# Split by pages
pages = text.split('=== PAGE ')
for p in pages:
    if not p.strip(): continue
    lines = [l.strip() for l in p.split('\n') if l.strip()]
    header = lines[0] if lines else ''
    content = ' '.join(lines[1:])
    p_num = header.split(' ===')[0] if ' ===' in header else '?'
    print(f"\n--- PAGE {p_num} ({len(content.split())} words) ---")
    print(content[:400] + '...')

# Let's check DAFTAR PUSTAKA entries
dp_index = clean_text.find('DAFTAR PUSTAKA')
if dp_index != -1:
    print("\n================ DAFTAR PUSTAKA ================")
    print(clean_text[dp_index:])

