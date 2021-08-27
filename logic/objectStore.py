from pathlib import Path

persons = []
inventoryItems = []
access_records = []


def get_existing_entries(records: dict) -> list:
    result = []
    history = records["history"]
    for record in history:
        p = Path(record["filePath"])
        if p.exists():
            result.append(record)
    return result


def update_history(records: dict):
    access_records.clear()
    record_entries = get_existing_entries(records)
    access_records.extend(record_entries)
