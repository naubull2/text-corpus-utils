import json
# Convert pretty printed JSON data back to .jsonl format

# JSONL pretty reader
def read_pretty_jsonl(filename):
    data = []
    current_json = ""

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            current_json += line.strip()

            try:
                # Try parsing the JSON object
                parsed_json = json.loads(current_json)
                data.append(parsed_json)

                # Reset the current JSON string
                current_json = ""
            except json.JSONDecodeError:
                pass

    return data
