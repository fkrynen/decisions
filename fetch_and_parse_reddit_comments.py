#!/usr/bin/env python3

""" scrape_em.py
    Fetch (top-level) reddit comments for posts specified in an input CSV
    and output them to a new CSV file with sentiment scores.
"""

import argparse
import codecs
import csv
import logging
import sys
from contextlib import closing
from pathlib import Path

import praw
import requests
from termcolor import colored as _colored
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

SHEET_ID = "1TlLFTgMX3CnDiMWqAugMcB3g9tofgI7VlPK2IPZCZpo"

INPUT_FILE = "Decision_SS.csv"
OUTPUT_FILE = "output.csv"

LINE_LENGTH = 80


def colored(text, *args, **kwargs):
    if sys.stdout.isatty():
        return _colored(text, *args, **kwargs)
    return text


def get_posts_from_google_sheet(sheet_id):
    sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    status_text = "\nReading URLs from Google Sheets..."
    print(colored(status_text, "yellow", attrs=["bold"]), end=" ", flush=True)

    with closing(requests.get(sheet_url, stream=True)) as _sh:
        reader = csv.DictReader(codecs.iterdecode(_sh.iter_lines(), "utf-8"))
        posts = [
            {"id": record["Clip # (.0)"], "url": record["Link to comments"]}
            for record in reader
            if record["Link to comments"]
        ]

    response_text = "done!"
    print(
        " " * (LINE_LENGTH - len(status_text) - 2 - len(response_text)),
        colored(response_text, "green", attrs=["bold"]),
        "\n",
    )

    return posts


def get_posts_from_csv(csv_input_file):
    status_text = f"\nReading URLs from {csv_input_file}..."
    print(colored(status_text, "yellow", attrs=["bold"]), end=" ", flush=True)

    with Path(csv_input_file).open("r") as _fh:
        reader = csv.DictReader(_fh)
        posts = [
            {"id": record["Clip # (.0)"], "url": record["Link to comments"]}
            for record in reader
            if record["Link to comments"]
        ]

    response_text = "done!"
    print(
        " " * (LINE_LENGTH - len(status_text) - 2 - len(response_text)),
        colored(response_text, "green", attrs=["bold"]),
        "\n",
    )

    return posts


def get_comments(posts, client_id, client_secret):

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent="praw:decisions:v0.1",
    )

    comments = []
    for post in posts:
        status_text = f"Getting comments for clip {post['id']}..."
        print(colored(status_text, "blue"), end=" ", flush=True)

        submission = reddit.submission(url=post["url"])
        submission.comments.replace_more(limit=0)
        for comment in submission.comments:
            comments.append(
                {
                    "clip_id": post["id"],
                    "post_url": post["url"],
                    "comment_id": comment.id,
                    "commentor": comment.author,
                    "comment": comment.body,
                    "comment_score": comment.score,
                }
            )

        response_text = f"{len(submission.comments)} retrieved!"
        print(
            " " * (LINE_LENGTH - len(status_text) - 3 - len(response_text)),
            colored(response_text, "green"),
        )
    return comments


def add_sentiment_scores(comments):

    naivebayes_analyzer = NaiveBayesAnalyzer()

    status_text = "Calculating sentiment scores..."
    print(colored(status_text, "magenta"), end="\r", flush=True)
    for i, comment in enumerate(comments, 1):
        sentiment_pattern = TextBlob(comment["comment"]).sentiment.polarity
        sentiment_naivebayes = TextBlob(
            comment["comment"], analyzer=naivebayes_analyzer
        ).sentiment

        comment.update(
            {
                "sentiment_pattern": "pos" if sentiment_pattern > 0 else "neg",
                "sentiment_pattern_score": sentiment_pattern,
                "sentiment_naivebayes": sentiment_naivebayes.classification,
                "sentiment_naivebayes_score": sentiment_naivebayes.p_pos
                if sentiment_naivebayes.classification == "pos"
                else 0 - sentiment_naivebayes.p_neg,
            }
        )
        response_text = f"{i} comments processed!"
        print(
            colored(status_text, "magenta"),
            " " * (LINE_LENGTH - len(status_text) - 3 - len(response_text)),
            colored(response_text, "green"),
            end="\r",
            flush=True,
        )

    print("\n")
    return comments


def write_comments_to_csv(comments, csv_output_file):
    status_text = f"Writing to {csv_output_file}..."
    print(
        colored(status_text, "yellow", attrs=["bold"]),
        end=" ",
        flush=True,
    )
    with Path(csv_output_file).open("w") as _fh:
        writer = csv.DictWriter(_fh, fieldnames=comments[0].keys())
        writer.writeheader()
        writer.writerows(comments)

    response_text = "done!"
    print(
        " " * (LINE_LENGTH - len(status_text) - 3 - len(response_text)),
        colored(response_text, "green", attrs=["bold"]),
    )


def main():
    """ Command-line entry-point. """

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(description="Description: {}".format(__file__))

    parser.add_argument("--client-id", action="store", help="Reddit API client_id")
    parser.add_argument(
        "--client-secret", action="store", help="Reddit API client_secret"
    )

    args = parser.parse_args()

    posts = get_posts_from_google_sheet(SHEET_ID)
    comments = get_comments(posts, args.client_id, args.client_secret)
    comments = add_sentiment_scores(comments)

    write_comments_to_csv(comments, OUTPUT_FILE)


if __name__ == "__main__":
    main()
