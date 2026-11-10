with open('docs/extracted_pdf_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

pages = text.split('=== PAGE ')
for p in pages:
    if not p.strip(): continue
    lines = [l.strip() for l in p.split('\n') if l.strip()]
    header = lines[0] if lines else ''
    content = '\n'.join(lines[1:])
    p_num = header.split(' ===')[0] if ' ===' in header else '?'
    print(f"\n#################### PAGE {p_num} ####################")
    print(content)

