# TODO: write this lmao

import gzip
import re
from io import FileIO

PATH = "enwiki-20240301-pagelinks.sql.gz"
HEADER_SIZE = 42

class Link():
    start: int
    end: int

    def __init__(self, start_id: int, end_id: int):
        self.start = start_id
        self.end = end_id

