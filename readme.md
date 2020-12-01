# NYC COVID-19 Testing Wait Times PDF Scraper

![request to create a scraper for nyc testing times](https://i.ibb.co/HDg0YSQ/image.png)

Challenge accepted!

This repo will automatically run the scraper every 15 minutes with a cronjob set up through GitHub Actions. Thanks to this [wonderful blog post](https://jasonet.co/posts/scheduled-actions/) from Jason Etcovitch that had most of the action automation setup I pulled from for the workflow.

The csv filenames are structured as `{two-hour time window}-{scrape timestamp}.csv`.

### Changelog

- 2020-11-30 21:07: Data now includes the time window as a column as well as the scrape time. The latest data is also stored in `latest.csv`. Corrected some data cleaning issues with characters being parsed incorrectly and newlines being included in the wait times column.
- 2020-11-30 21:14: Data moved to the `data` folder, copy of `latest.csv` included in root dir.
- 2020-12-01 08:28: Added `md5` hash of PDF content to check if PDF is a new file. If not a new file, don't parse or add a new csv.