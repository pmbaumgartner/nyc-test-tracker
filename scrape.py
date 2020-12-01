import camelot
import requests
from tempfile import NamedTemporaryFile
from datetime import datetime

r = requests.get(
    "https://hhinternet.blob.core.windows.net/wait-times/testing-wait-times.pdf"
)
with NamedTemporaryFile(suffix=".pdf") as temppdf:
    temppdf.write(r.content)
    tables = camelot.read_pdf(temppdf.name, flavor="stream")

scrape_timestamp = datetime.now()

df = tables[0].df
date = df.loc[0, 3].replace(" |", ", ").replace("/", "-")
df_data = df.loc[1:, :].copy()

melted_data = df_data.melt()
melted_data["time"] = (melted_data.index % 2).map({0: "Location", 1: "Wait"})
pivoted_data = melted_data[["value", "time"]].pivot(columns="time")
pivoted_data.columns = ["Location", "Wait"]
pivoted_data["Location"] = pivoted_data["Location"].fillna(method="ffill")
pivoted_data = pivoted_data.dropna()
pivoted_data["Location"] = (
    pivoted_data["Location"]
    .str.replace("\n", "", regex=False)
    .str.replace("(cid:415)", "ti", regex=False)
    .str.replace("(cid:425)", "tt", regex=False)
)
pivoted_data["Wait"] = pivoted_data["Wait"].str.replace("\n", "", regex=False)
pivoted_data["Time Window"] = date
pivoted_data["Scrape Timestamp"] = scrape_timestamp
pivoted_data = pivoted_data.reset_index(drop=True)

pivoted_data.to_csv(f"data/{date}-{scrape_timestamp}.csv")
pivoted_data.to_csv(f"data/latest.csv")
pivoted_data.to_csv(f"latest.csv")
