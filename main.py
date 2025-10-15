# ruff: noqa
# type: ignore
# # pylint: disable-all
# %%
import zipfile
from pathlib import Path
import mailbox
import shutil
from email.parser import BytesParser
from email import policy
import mailparser
from pprint import pprint
import sqlite3
import re
import pandas as pd

working_directory = Path(__file__).parent.resolve()
extracts_dir = working_directory / "extracts"
mailbox_dir = extracts_dir / "mailboxes"
attachment_dir = extracts_dir / "bills"
management_dir = extracts_dir / "management"
db_path = management_dir / "claims.db"

mailbox_paths = []

zips = [
    r"""E:\Projects\aesthetics_processor\takeout-20251014T165526Z-1-001.zip""",
    r"""E:\Projects\aesthetics_processor\takeout-20251014T165627Z-1-001.zip""",
]

sample_letter = None
sample_mailbox = None
sample_subjects = []
sample_letters = []


def next_available_filename(target_file: Path) -> Path:
    if not target_file.exists():
        return target_file

    stem, suffix = target_file.stem, target_file.suffix
    index = 2
    while True:
        candidate = target_file.with_name(f"{stem}_{index}{suffix}")
        if not candidate.exists():
            return candidate
        index += 1


def create_directories():
    paths = [
        extracts_dir,
        mailbox_dir,
        attachment_dir,
        management_dir,
    ]
    for location in paths:
        Path.mkdir(location, parents=True, exist_ok=True)


# %%


def get_final_item_path(filename, replace_files=False):
    item_name = Path(filename).name
    item_path = extracts_dir / item_name
    if replace_files:
        return item_path
    final_path = next_available_filename(item_path)
    return final_path


def extract_zips(replace_files=True):
    for zipf in zips:
        zip_path = Path(zipf)
        if not zip_path.is_file():
            print(f"{zip_path} was not found")
            continue

        with zipfile.ZipFile(zipf, "r") as archive:
            for item in archive.infolist():
                if item.is_dir():
                    continue
                file_path = get_final_item_path(Path(item.filename), replace_files)
                with archive.open(item, "r") as src, open(file_path, "wb") as dst:
                    shutil.copyfileobj(src, dst)

                if file_path.suffix.lower() == ".mbox" or file_path.name == "mbox":
                    mailbox_paths.append(file_path)


def process_message(letter):
    # sample_letter = letter
    eletter = mailparser.parse_from_bytes(letter.as_bytes())
    sample_letter = eletter
    sample_letters.append(eletter)

    sample_subjects.append(eletter.subject)


def process_mailboxes():
    for mbox_file in mailbox_paths:
        open_mailbox(mbox_file)


def open_mailbox(mailbox_path):
    mbox_file = mailbox.mbox(mailbox_path)
    sample_mailbox = mbox_file

    for index, letter in mbox_file.items()[0:10]:
        process_message(letter)


def init_db(db_path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS treatments (
                 id INTEGER PRIMARY KEY AUTOINCREMENT)
                 """)


# %%
create_directories()
extract_zips()
process_mailboxes()
