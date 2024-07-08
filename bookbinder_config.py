import time

INPUT = "input/stj/1t_dec.jsonl"
OUTPUT = f"output/stj/{int(time.time())}.jsonl"

PAGE_MATCH = r"^Page \d{1,3}"

REMOVALS = [
    r"</table>",
    r"<table.*>",
    r"</tr>",
    r"<tr.*>",
    r"</td>",
    r"<td.*>",
]
