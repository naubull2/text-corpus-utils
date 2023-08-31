import re

from tabulate import tabulate


def parse_markdown_table(markdown_text):
    # Find the first markdown table in the text
    table_match = re.search(r"(\|.*\|?(\n|$)){3,}", markdown_text, re.U)

    if table_match:
        markdown_table = table_match.group(0)
        rows = markdown_table.strip().split("\n")

        # Extract the header row and divide it into column headers
        header_row = rows[0]
        if header_row.strip().endswith("|"):
            column_headers = [c.strip() for c in header_row.split("|")[1:-1]]
        else:
            column_headers = [c.strip() for c in header_row.split("|")[1:]]
        table_width = len(column_headers)

        # Keep cell alignments
        cell_align = [
            re.sub(r"-{2,}", "---", c.strip()) for c in rows[1].split("|")[1:]
        ][:table_width]

        # Extract and process each data row
        table_data = [column_headers, cell_align]
        for row in rows[2:]:
            row_data = [c.strip() for c in row.split("|")[1:]][:table_width]
            table_data.append(row_data)

        # Remove trailing empty rows
        _row = table_data[-1]
        while not _row:
            table_data = table_data[:-1]
            if table_data:
                _row = table_data[-1]
            else:
                break

        idx_range = table_match.span()
        return table_data, idx_range
    else:
        # No markdown table found in the input
        return None, None


def simplify_markdown_table(text):
    # Recursively find and parse markdown tables
    table, idx_range = parse_markdown_table(text)
    if table is not None:
        # render into simplified form and replace the text
        new_table = []
        for row in table:
            new_table.append(f"| {' | '.join(row)} |")

        if text[idx_range[1] :]:
            text = (
                text[: idx_range[0]]
                + "\n".join(new_table)
                + "\n"
                + simplify_markdown_table(text[idx_range[1] :])
            )
        else:
            text = text[: idx_range[0]] + "\n".join(new_table)

    return text


def prettify_markdown_table(text):
    # Recursively find and parse markdown tables
    table, idx_range = parse_markdown_table(text)

    def get_colalign(align_row):
        alignment = []
        for e in align_row:
            if ":---:" in e:
                alignment.append("center")
            elif ":---" in e:
                alignment.append("left")
            elif "---:" in e:
                alignment.append("right")
            else:
                alignment.append("global")
        return alignment

    if table is not None:
        new_table = tabulate(
            table[2:], table[0], tablefmt="pipe", colalign=get_colalign(table[1])
        )

        if text[idx_range[1] :]:
            text = (
                text[: idx_range[0]]
                + new_table
                + "\n"
                + prettify_markdown_table(text[idx_range[1] :])
            )
        else:
            text = text[: idx_range[0]] + new_table

    return text


if __name__ == "__main__":
    markdown_text = """
Take a look at the following table
| Difference                                          | Japan               | Korea            |
| -------------------------------------------- | ----------------------- | ------------------ |
| A                                            | Japan is ..             | Korea is ...       |
| Purpose                    | To maintain ..          | To preserve .. |
So we've seen how two countries differ..
However,

Take a look at the following table

| Difference           | Japan | Korea 
| :----------------------------- | :---: | ----
| A     | Japan is ..      | Korea is ...  
| Purpose    | To maintain ..    | To preserve ..

Can you spot a difference?
"""

    text = simplify_markdown_table(markdown_text)
    print("======= Minimal md-table =========")
    print(text)
    print("======== Pretty md-table =========")
    print(prettify_markdown_table(text))
