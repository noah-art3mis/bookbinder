import re
import time

INPUT = "input/MTG/content/ch02.xml"
OUTPUT = f"output/{int(time.time())}.txt"

PAGE_MATCH = r"^Page \d{1,3}"

REMOVALS = [
    r"</table>",
    r"<table.*>",
    r"</tr>",
    r"<tr.*>",
    r"</td>",
    r"<td.*>",
]


def cleanup(lines):
    output = []
    for line in lines:

        line = line.strip()

        # remove ftvr (no n)
        line = re.sub("[\f\t\v\r]+", " ", line)

        # remove markup tags
        line = line.replace("<.*?>", "")

        # remove page numbers
        line = re.sub(PAGE_MATCH, "", line)

        # remove roman numeral pages
        # line = re.sub("^ *[mdclxvi]+ *$", "", line)

        # remove running head
        # line = re.sub("^ *\w{1} *$", "", line)

        # if re.match("^.{54,}$", line):
        # line = line.strip()

        # project specific cleanup
        for pattern in REMOVALS:
            line = re.sub(pattern, "", line)

        # line = re.sub("::: *\w*", "", line)  # ::: ~
        # line = re.sub("\{.*?\}", "", line)  # {~}
        # line = re.sub("\[\]", "", line)  # []
        # line = re.sub("```", "", line)  # ´´´
        # line = re.sub("<\/p>", "", line)  # </p>

        # remove double space
        line = re.sub(" +", " ", line)

        output.append(line + "\n")

    return output


def main():
    with open(INPUT, "r", encoding="utf-8") as _input:
        lines = _input.readlines()

    lines = [line for line in lines if line.strip()]
    result = cleanup(lines)
    result = [line for line in result if line.strip()]

    with open(OUTPUT, "w", encoding="utf-8") as _output:
        _output.writelines(result)
        print("Antiquarian: cleanup complete. Output written to", OUTPUT)


if __name__ == "__main__":
    main()
