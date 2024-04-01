"""
converts wikidump compressed mysqldump database dumps of wikipedia's `page` table into compressed plaintext databases 
that can be used in the app. removes all data not used in our project.
"""

import re
from io import FileIO
from datatypes import Page, DatabaseInfo

def convert_db_block(block: str, pattern: str) -> list[Page]:
    out_list = []
    page_strings = block[27:-3].split("),(")
    p = re.compile(pattern)
    for page_string in page_strings:
        r = p.search(page_string)
        try:
            out_list.append(Page(
                int(r.group(1)),        # page id
                int(r.group(2)),        # namespace (we only care if its zero but just save the int for now)
                r.group(3),             # page title (slice to remove single-quotes in string)
                r.group(4) == "1"))     # if page is a redirect page
        except:
            pass

    return out_list

def check_valid_block(block: str) -> bool:
    return block[:25] == "INSERT INTO `page` VALUES"

def write_pages_to_file(pages: list[Page], file: FileIO) -> None:
    for page in pages:
        if page.is_valid():
            file.write(f"{page.page_id} {page.title}\n")


def make_db(db_file: FileIO, out_file: FileIO, db_info: DatabaseInfo) -> None:
    for i in range(db_info.header_size):
        db_file.readline()

    while True:
        block = str(db_file.readline(), 'utf-8')
        if not check_valid_block(block):
            break
        pages = convert_db_block(block, db_info.pattern)
        write_pages_to_file(pages, out_file)


def add_to_ns0_dict(pages: list[Page], ns0_dict: dict[str, int]) -> None:
    for page in pages:
        if page.is_ns0():
            ns0_dict[page.title] = page.page_id


def make_ns0_dict(db_file: FileIO, db_info: DatabaseInfo) -> dict[str, int]:
    for i in range(db_info.header_size):
        db_file.readline()

    out_dict = {}
    while True:

        block = str(db_file.readline(), 'utf-8')
        if not check_valid_block(block):
            break
        pages = convert_db_block(block, db_info.pattern)
        add_to_ns0_dict(pages, out_dict)
    
    return out_dict


# extra stuff

def reverse_db_file(db_file: FileIO, out_file: FileIO) -> None:
    while True:
        line = str(db_file.readline().strip())
        if line == "":
            break
        data = line.split(" ")
        out_file.write(f"{data[1]} {data[0]}\n")


def sort_db(in_file: FileIO, out_file: FileIO) -> None:
    db_dict = {}
    for line in in_file:
        data = str(line).strip().split(" ")
        db_dict[data[0]] = data[1]
    
    db_dict = dict(sorted(db_dict.items()))

    for key in db_dict:
        out_file.write(f"{key} {db_dict[key]}\n")

def print_stats(file: FileIO, header_size: int) -> None:
    valid_pages = 0
    total_pages = 0
    file_size = 0

    print("skipping header")
    for i in range(header_size):
        file.readline()
    
    print("starting calculations")
    n = 0
    while True:
        if (n % 20 == 0 and n > 0):
            print("proportion of valid pages as of block " + str(n) + ": " + str(valid_pages / total_pages))
        n += 1

        block = str(file.readline(), 'utf-8')
        if not check_valid_block(block):
            break
        pages = convert_db_block(block)
        valid_pages += count_valid(pages)
        total_pages += len(pages)
        file_size += estimate_file_size(pages)
    
    print("\ndone! final stats:")
    print("number of database data block: " + str(n))
    print("\nnumber of total pages: " + str(total_pages))
    print("number of valid pages: " + str(valid_pages))
    print("proportion of valid pages: " + str(valid_pages / total_pages))
    print("\nfile size estimation: " + str(file_size) + " bytes, or " + str(round(file_size / 1000000, 1)) + " MB")

def estimate_file_size(pages: list[Page]) -> int:
    size = 0
    for page in pages:
        if page.is_valid():
            size +=  len(str(page.page_id)) + len(page.title) + 2 # the length of the strings we're storing, add "\n" and " "
    return size

def count_valid(pages: list[Page]) -> float:
    count = 0
    for page in pages:
        if page.is_valid():
            count += 1
    return count