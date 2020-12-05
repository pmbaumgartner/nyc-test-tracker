import hashlib
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

import camelot
import pandas as pd
import requests


def value_parser(cell: str):
    values = [
        value.replace("(cid:415)", "ti").replace("(cid:425)", "tt").replace("ﬀ", "ff")
        for value in cell.split("\n")
    ]
    labels = ["Location", "Wait", "Last Updated"]
    return dict(zip(labels, values))


r = requests.get(
    "https://hhinternet.blob.core.windows.net/wait-times/testing-wait-times.pdf"
)
scrape_timestamp = datetime.now()

pdf_hash = hashlib.md5(r.content).hexdigest()
hash_location = Path("md5")
if hash_location.exists():
    new_file = hash_location.read_text() != pdf_hash
else:
    new_file = True

if new_file:
    hash_location.write_text(pdf_hash)
    with NamedTemporaryFile(suffix=".pdf") as temppdf:
        temppdf.write(r.content)
        tables = camelot.read_pdf(
            temppdf.name,
            flavor="stream",
            row_tol=30,
            table_areas=["41,453,751,153"],
            layout_kwargs={"detect_vertical": False},
        )

    all_values = tables[0].df.values.ravel()
    parsed_values = [value_parser(cell) for cell in all_values]
    df = pd.DataFrame(parsed_values)

    df.to_csv(f"data/{scrape_timestamp}.csv")
    df.to_csv("data/latest.csv")
    df.to_csv("latest.csv")
