# decisions

This repo contains a python application which will:

- download and parse content from a Google Spreadsheet
- extract a column of Reddit post URLs from that spreadsheet
- connect to the Reddit API and retrieve (top-level) comments for each post
- pass those comments through two different sentiment-analysis models
- output the assembled comments and sentiment scores to a new CSV file

## Installation / Usage

Reddit API credentials are required: get them [here](https://www.reddit.com/prefs/apps) (use the "create another app" button at the bottom).

- Clone this repo
- Make sure pipenv is installed (`pip install pipenv`)
- `pipenv install`
- `pipenv run python fetch_and_parse_reddit_comments.py --client-id <client_id> --client-secret <client_secret>`

To use a local CSV file instead of a remote Google Sheet toggle [these lines](https://github.com/simonwiles/decisions/blob/4e28525989c2a533eda1c96df9dea93c2c2ed005/fetch_and_parse_reddit_comments.py#L183-L184)
The `SHEET_ID`/`INPUT_FILE` and `OUTPUT_FILE` are hardcoded at the top of the script.

## Notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/16egGLoL3_I308sxRdpoKkZjk9x1FZvXZ)

There is also a Google Colab notebook that runs this code:
https://colab.research.google.com/drive/16egGLoL3_I308sxRdpoKkZjk9x1FZvXZ

The notebook will source this module directly from GitHub and bootstrap `pipenv` to install the dependencies, which is kinda interesting in its own right.
