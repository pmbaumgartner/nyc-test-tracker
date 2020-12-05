from pathlib import Path
import pandas as pd
from playwright import sync_playwright
from time import sleep

with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.newPage()
    page.goto(
        "https://hhinternet.blob.core.windows.net/wait-times/testing-wait-times.pdf",
        waitUntil="networkidle",
    )
    sleep(1)
    page.screenshot(path="docs/screenshot.png")
    browser.close()

HTML_FRONT = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta http-equiv="x-ua-compatible" content="ie=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />

    <title>NYC Testing Times Tracker</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,300italic,700,700italic">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/milligram/1.3.0/milligram.css">
  </head>

  <body>
    <div class="container">
    <h1>NYC Testing Times Tracker</h1>
"""


HTML_END = """
    <p><a href="https://hhinternet.blob.core.windows.net/wait-times/testing-wait-times.pdf">source</a></p>
    <p>PDF at time of scrape<img src="screenshot.png"></p>
    </div>
  </body>
</html>
"""

df = pd.read_csv("latest.csv", index_col=0)
df_html = df.to_html(index=False, bold_rows=False, border=False, justify="left")

table_page = HTML_FRONT + df_html + HTML_END

Path("docs/index.html").write_text(table_page)
