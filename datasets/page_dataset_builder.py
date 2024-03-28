"""
converts wikidump compressed mysqldump database dumps of wikipedia's `page` table into compressed plaintext databases 
that can be used in the app. removes all data not used in our project.

TODO:
    - add something that converts links to pages with redirects into a link directly
      to the page that the redirect page links to (saves on db size)
"""
import gzip
import re
from io import FileIO

PATH = "enwiki-20240301-page.sql.gz"
HEADER_SIZE = 50

class Page():
    page_id: int
    _namespace: int
    title: str
    _is_redirect: bool
    
    def __init__(self, page_id: int, namespace: int, title: str, is_redirect: bool) -> None:
        self.page_id = page_id
        self._namespace = namespace
        self.title = title
        self._is_redirect = is_redirect

    def __str__(self) -> str:
        return f"{self.page_id},{self._namespace},{self.title},{1 if self.is_redirect else 0}"
    
    def is_valid(self) -> bool:
        return self._namespace == 0 and not self._is_redirect
    
    def is_valid_redirect(self) -> bool:
        return self._namespace == 0 and self._is_redirect
    
    def is_ns0(self) -> bool:
        return self._namespace == 0

def convert_db_block(block: str) -> list[Page]:
    out_list = []
    page_strings = block[27:-3].split("),(")
    p = re.compile("(\d+),(\d+),'(.+?)',(\d+),")
    for page_string in page_strings:
        r = p.search(page_string)
        try:
            out_list.append(Page(
                int(r.group(1)),        # page id
                int(r.group(2)),        # namespace (we only care if its zero but just save the int for now)
                r.group(3),             # page title (slice to remove single-quotes in string)
                r.group(4) == "1"))     # if page is a redirect page
        except:
            print('fuck shit page conversion broke, heres the page string')
            print(page_string)

    return out_list


def count_valid(pages: list[Page]) -> float:
    count = 0
    for page in pages:
        if page.is_valid():
            count += 1
    return count


def check_valid_block(block: str) -> bool:
    return block[:25] == "INSERT INTO `page` VALUES"


def estimate_file_size(pages: list[Page]) -> int:
    size = 0
    for page in pages:
        if page.is_valid():
            size += len(str(page.page_id)) + len(page.title) + 2 # the length of the strings we're storing, add "\n" and " "
    return size


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


def write_pages_to_file(pages: list[Page], file: FileIO) -> None:
    for page in pages:
        if page.is_valid():
            file.write(f"{page.page_id} {page.title}\n")


def write_db_file(db_file: FileIO, out_file: FileIO, header_size: int) -> None:
    
    print("progress: skipping header")
    for i in range(header_size):
        db_file.readline()

    print("progress: starting calculations")
    n = 0
    while True:
        if (n % 20 == 0 and n > 0):
            print("progress: working on block " + str(n))
        n += 1

        block = str(db_file.readline(), 'utf-8')
        if not check_valid_block(block):
            break
        pages = convert_db_block(block)
        write_pages_to_file(pages, out_file)
    
    print("done! file has been written.")


def add_to_redirect_set(pages: list[Page], rd_set: set[int]) -> None:
    for page in pages:
        if page.is_valid_redirect():
            rd_set.add(page.page_id)


def make_redirect_set(db_file: FileIO, header_size: int) -> set[int]:

    print("progress: skipping header")
    for i in range(header_size):
        db_file.readline()

    print("progress: starting calculations")
    out_set = set()
    n = 0
    while True:
        if (n % 20 == 0 and n > 0):
            print("progress: working on block " + str(n))
        n += 1

        block = str(db_file.readline(), 'utf-8')
        if not check_valid_block(block):
            break
        pages = convert_db_block(block)
        add_to_redirect_set(pages, out_set)

    
    print("done! set is made.")
    return out_set


def add_to_ns0_dict(pages: list[Page], ns0_dict: dict[str, int]) -> None:
    for page in pages:
        if page.is_ns0():
            ns0_dict[page.title] = page.page_id


def make_ns0_dict(db_file: FileIO, header_size: int) -> dict[str, int]:

    print("progress: skipping header")
    for i in range(header_size):
        db_file.readline()

    print("progress: starting calculations")
    n = 0
    out_dict = {}
    while True:
        if (n % 20 == 0 and n > 0):
            print("progress: working on block " + str(n))
        n += 1

        block = str(db_file.readline(), 'utf-8')
        if not check_valid_block(block):
            break
        pages = convert_db_block(block)
        add_to_ns0_dict(pages, out_dict)
    
    print("done! dict is made.")
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


def main():
    # uncomment if you'd like to get some stats on the wikipedia dataset
    # with gzip.open(PATH, "r") as file:
    #     print_stats(file, HEADER_SIZE)

    # create db file 
    with gzip.open(PATH, "r") as db, open("pages.txt", "w") as out:
        write_db_file(db, out, HEADER_SIZE)

    # create reverse database
    # with open("pages.txt", "r") as db_file, open("pages-rev.txt", "w") as out_file:
    #     reverse_db_file(db_file, out_file)

    # sort reversed database
    # with open("pages-rev.txt", "r") as in_file, open("pages-rev-sorted.txt", "w") as out_file:
    #     sort_db(in_file, out_file)

if __name__ == "__main__":
    main()