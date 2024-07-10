import re

def parse_code_blocks(markdown):
    code_blocks = re.findall(r'```json(?:[a-zA-Z]*)\n([\s\S]*?)\n```', markdown)
    if not code_blocks:
        raise ValueError("No code blocks found")
    all_arrays = []
    for code_block in code_blocks:
        all_arrays.append(code_block.strip())
    return all_arrays
