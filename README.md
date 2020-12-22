# decisions

This repo contains a python application which will:

- download and parse content from a Google Spreadsheet
- extract a column of Reddit post URLs from that spreadsheet
- connect to the Reddit API and retrieve (top-level) comments for each post
- pass those comments through two different sentiment-analysis models
- output the assembled comments and sentiment scores to a new CSV file

## Notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/16egGLoL3_I308sxRdpoKkZjk9x1FZvXZ)

There is also a Google Colab notebook that runs this code:
https://colab.research.google.com/drive/16egGLoL3_I308sxRdpoKkZjk9x1FZvXZ

The notebook will source this module directly from GitHub and bootstrap `pipenv` to install the dependencies.
