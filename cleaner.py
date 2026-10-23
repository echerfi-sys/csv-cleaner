import sys
import csv


def read_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def write_rows(rows, path):
    if not rows:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

        
def drop_empty_rows(rows):
    return [row for row in rows if any(value.strip() for value in row.values())]

def strip_whitespace(rows):
    return [{key.strip(): value.strip() for key, value in row.items()} for row in rows]


def remove_duplicates(rows):
    seen = set()
    result = []
    for row in rows:
        key = tuple(row.items())
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result



def normalize_city(rows):
    return [{**row, "city": row["city"].capitalize()} for row in rows]

def clean(rows):
    rows = drop_empty_rows(rows)
    rows = strip_whitespace(rows)
    rows = normalize_city(rows)
    return remove_duplicates(rows)


if __name__ == "__main__":
    input_path, output_path = sys.argv[1], sys.argv[2]
    rows = clean(read_rows(input_path))
    write_rows(rows, output_path)
    print(f"{len(rows)} rows written to {output_path}")
