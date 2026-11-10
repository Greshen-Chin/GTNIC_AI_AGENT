import re

with open('docs/extracted_pdf_text.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize spacing
lines = [l.strip() for l in text.split('\n') if l.strip()]
clean_text = ' '.join(lines)
clean_text = re.sub(r'\s+', ' ', clean_text)

# Let's find every citation pattern: [1], [2], (1), author names, etc.
citations_to_check = {
    1: ["16 Serangan Siber", "16 serangan", "Riset:", "[1]"],
    2: ["Haryanto", "1,5 Miliar", "detikInet", "[2]"],
    3: ["IBM", "4,88 juta", "Cost of a Data Breach", "[3]"],
    4: ["ISC2", "Workforce Study", "defisit talenta", "[4]"],
    5: ["MITRE", "ATT&CK", "[5]"],
    6: ["OWASP", "Top 10", "[6]"],
    7: ["UU PDP", "UU No. 27", "Pasal 46", "[7]"],
    8: ["Pusat Data Nasional", "PDNS", "Brain Cipher", "[8]"],
    9: ["ReAct", "Yao", "[9]"],
    10: ["Kominfo", "Telkom", "Siaran Pers", "[10]"],
    11: ["SANS", "SOC Survey", "[11]"]
}

for num, terms in citations_to_check.items():
    print(f"\n--- Checking Ref [{num}] ---")
    found = False
    for term in terms:
        matches = list(re.finditer(re.escape(term), clean_text, re.IGNORECASE))
        if matches:
            found = True
            for m in matches:
                start = max(0, m.start() - 60)
                end = min(len(clean_text), m.end() + 60)
                snippet = clean_text[start:end].replace('\n', ' ')
                # Check if it's in DAFTAR PUSTAKA
                is_in_dp = m.start() > clean_text.find('DAFTAR PUSTAKA')
                loc = "DAFTAR PUSTAKA" if is_in_dp else "BODY TEXT"
                print(f"  [{loc}] '{term}': ...{snippet}...")
    if not found:
        print(f"  NOT FOUND IN ENTIRE DOCUMENT!")

