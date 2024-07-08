import re
from json import loads
from bookbinder_config import INPUT, OUTPUT, PAGE_MATCH, REMOVALS


def main():
    with open(OUTPUT, "w", encoding="utf-8") as outfile:
        with open(INPUT, "r", encoding="utf-8") as infile:
            for line in infile:
                json_line = loads(line)
                json_line = json_line["decisao"]
                json_line = cleanup(json_line)

                outfile.write(json_line + "\n")

    print("Antiquarian: cleanup complete. Output written to", OUTPUT)


def cleanup(line: str) -> str:
    line = line.strip()

    # remove ftvr (no n)
    line = re.sub("[\f\t\v\r]+", " ", line)

    # remove line breaks
    line = re.sub("\n", " ", line)

    # remove markup tags
    # line = line.replace("<.*?>", "")

    # remove page numbers
    # line = re.sub(PAGE_MATCH, "", line)

    # remove roman numeral pages
    # line = re.sub("^ *[mdclxvi]+ *$", "", line)

    # remove running head
    # line = re.sub("^ *\w{1} *$", "", line)

    # if re.match("^.{54,}$", line):
    # line = line.strip()

    # project specific cleanup
    # for pattern in REMOVALS:
    #     line = re.sub(pattern, "", line)

    # line = re.sub("::: *\w*", "", line)  # ::: ~
    # line = re.sub("\{.*?\}", "", line)  # {~}
    # line = re.sub("\[\]", "", line)  # []
    # line = re.sub("```", "", line)  # ´´´
    # line = re.sub("<\/p>", "", line)  # </p>

    # remove double space
    line = re.sub(" +", " ", line)

    return line


if __name__ == "__main__":
    main()
