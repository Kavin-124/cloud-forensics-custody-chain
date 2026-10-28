with open("expand_chapters_to_maximum.py", "r", encoding="utf-8") as f:
    text = f.read()

# The content is between massive_content = ''' and the last '''
start_marker = "massive_content = '''"
start_pos = text.find(start_marker)
if start_pos != -1:
    content = text[start_pos + len(start_marker):]
    end_pos = content.rfind("'''")
    if end_pos != -1:
        content = content[:end_pos]
    with open("generate_chapters_content.py", "w", encoding="utf-8") as out_f:
        out_f.write(content.strip() + "\n")
    print("Successfully extracted code!")
else:
    print("Start marker not found!")
