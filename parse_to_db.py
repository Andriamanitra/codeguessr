from collections.abc import Iterator
import re
import sys
import sqlite3

from lxml import etree


HEADER_REGEX = re.compile(r"\|([^}]+)}}")
def get_header_lang(line: str) -> str:
    """
    Examples:
    >>> get_header_lang("=={{header|C}}==")
    'C'
    >>> get_header_lang("=={{header|Icon}} and {{header|Unicon}}==")
    'Icon'
    >>> get_header_lang("=={{header|F_Sharp|F#}}==")
    'F#'
    """
    header_langs = HEADER_REGEX.findall(line)
    if header_langs == []:
        raise ValueError(f"Invalid header '{line}'")
    if len(header_langs) > 1:
        print(f"  WARNING: weird header '{line.strip()}'", file=sys.stderr)
    return header_langs[0].strip()


def find_solutions(text: str, is_esolang: bool = False) -> Iterator[tuple[str, str]]:
    """
    Iterate through Rosetta code mediawiki text, yielding tuples of form
    ('LANGUAGE_NAME', 'CODE\n...') along the way

    The text starts with a short description of the task, then there are multiple
    sections for solutions in various languages. Each section starts with a header
    line, like one of these:
    =={{header|C}}==
    =={{header|Icon}} and {{header|Unicon}}==
    =={{header|F_Sharp|F#}}==

    slightly different headers for FizzBuzz/EsoLang and 99 Bottles of Beer/EsoLang pages:
    ===Chef===
    ===Whitespace===
    
    After a header there may be code block or multiple code blocks that look
    something like this:
    <syntaxhighlight lang="c">#include <stdio.h>
    int main(int argc, char **argv) {
      return 0;
    }</syntaxhighlight>

    This function should yield a solution (a tuple of language and code, with
    the language from most recently encountered "{{header|...}}") for each of
    these code blocks.

    Sometimes there are shorter snippets of code inline (meaning the line does
    not start with "<syntaxhighlight") but currently they are just ignored
    as they would complicate the parsing (and snippets that short are not
    interesting for our purposes anyway).
    """

    # this is not an efficient way to build lots of multiline strings but should
    # be fine for a script that gets ran once in a blue moon
    code = ""
    language = None
    for line in text.splitlines(keepends=True):
        if code:
            if "</syntaxhighlight>" not in line:
                code += line
            else:
                code_end, _endtag, _rest = line.partition("</syntaxhighlight>")
                code += code_end
                if language is None:
                    print("  WARNING: Encountered code block outside headered section, ignoring", file=sys.stderr)
                else:
                    yield (language, code.removeprefix("\n"))
                code = ""
        else:
            # check for header containing language name
            if line.startswith("=={{header|"):
                language = get_header_lang(line)
            elif is_esolang and line.startswith("==="):
                language = line.strip().removeprefix("===").removesuffix("===")
            # start of code block
            if line.startswith("<syntaxhighlight") and "</syntaxhighlight>" not in line:
                _, _, code = line.partition(">")


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS solutions(
    id INTEGER PRIMARY KEY,
    ts TIMESTAMP,
    task_name VARCHAR,
    lang VARCHAR,
    code VARCHAR
)
"""

def main(xml_file_name: str, db_file_name: str = "rosettacodes.db"):
    et = etree.parse(xml_file_name)
    root = et.getroot()
    pages = root.findall("page", namespaces=root.nsmap)
    solution_id = 1000
    with sqlite3.connect(db_file_name) as conn:
        conn.execute(CREATE_TABLE_SQL)
        for page in pages:
            task_name = page.findtext("title", namespaces=root.nsmap)
            revision = page.find("revision", namespaces=root.nsmap)
            timestamp = revision.findtext("timestamp", namespaces=root.nsmap)
            format = revision.findtext("format", namespaces=root.nsmap)
            assert format == "text/x-wiki", f"Error: Unknown format '{format}'"
            text = revision.findtext("text", namespaces=root.nsmap)
            print("PROCESSING TASK:", task_name, file=sys.stderr)
            is_esolang = task_name.endswith("/EsoLang")
            for language, code in find_solutions(text, is_esolang=is_esolang):
                conn.execute(
                    "INSERT INTO solutions(id, ts, task_name, lang, code)" \
                    " VALUES(?, ?, ?, ?, ?)",
                    (
                        solution_id,
                        timestamp,
                        task_name,
                        language,
                        code
                    )
                )
                solution_id += 1


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            "",
            "Usage: python3 parse_to_db.py XMLFILE [SQLITE_DB]",
            "",
            "  Get the XML file from https://rosettacode.org/wiki/Special:Export",
            "  by adding pages from category 'Programming Tasks'.",
            "",
            sep="\n"
        )
    else:
        main(*sys.argv[1:])
