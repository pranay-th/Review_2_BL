import json
import csv
import io
import aiofiles


class FileHandler:
    def __init__(self, json_path, csv_path):
        self.json_path = json_path
        self.csv_path = csv_path

    def read_json(self):
        try:
            with open(self.json_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def write_json(self, tasks):
        with open(self.json_path, "w") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4)

    def write_csv(self, tasks):
        with open(self.csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "title", "priority", "status"])
            writer.writeheader()
            for t in tasks:
                writer.writerow(t.to_dict())

    async def async_write_json(self, tasks):
        data = json.dumps([t.to_dict() for t in tasks], indent=4)
        async with aiofiles.open(self.json_path, "w") as f:
            await f.write(data)

    async def async_write_csv(self, tasks):
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=["id", "title", "priority", "status"])
        writer.writeheader()
        for t in tasks:
            writer.writerow(t.to_dict())
        async with aiofiles.open(self.csv_path, "w") as f:
            await f.write(buffer.getvalue())
