with open("generate_chapters_content.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.strip().startswith('code_snippet = ('):
        skip = True
        new_lines.append('    try:\n')
        new_lines.append('        with open("crypto_chain.py", "r", encoding="utf-8") as f_src:\n')
        new_lines.append('            code_snippet = f_src.read()[:2500]\n')
        new_lines.append('    except Exception:\n')
        new_lines.append('        code_snippet = "# Refer to crypto_chain.py in project repository"\n')
        new_lines.append('    code_snippet = "".join(c for c in code_snippet if c in "\\t\\n\\r" or ord(c) >= 32)\n')
        continue
    if skip and line.strip().startswith('p_code = doc.add_paragraph()'):
        skip = False

    if not skip:
        new_lines.append(line)

with open("generate_chapters_content.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Appendix successfully updated via fix_appendix.py!")
