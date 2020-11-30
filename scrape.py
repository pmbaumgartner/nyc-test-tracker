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
    .str.replace("(cid:415)", "", regex=False)
)
pivoted_data = pivoted_data.reset_index(drop=True)

pivoted_data.to_csv(f"{date}-{datetime.now()}.csv")
