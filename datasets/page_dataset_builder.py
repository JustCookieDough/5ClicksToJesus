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
    namespace: int
    title: str
    is_redirect: bool
    
    def __init__(self, page_id: int, namespace: int, title: str, is_redirect: bool) -> None:
        self.page_id = page_id
        self.namespace = namespace
        self.title = title
        self.is_redirect = is_redirect

    def __str__(self) -> str:
        return f"{self.page_id},{self.namespace},{self.title},{1 if self.is_redirect else 0}"
    
    def is_valid(self) -> bool:
        return self.namespace == 0 and not self.is_redirect


def convert_db_line(line: str) -> list[Page]:
    out_list = []
    page_strings = line[27:-3].split("),(")
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
            print('fuck shit line conversion broke, heres the page string')
            print(page_string)

    return out_list


def count_valid(pages: list[Page]) -> float:
    count = 0
    for page in pages:
        if page.is_valid():
            count += 1
    return count


def check_valid_line(line: str) -> bool:
    return line[:25] == "INSERT INTO `page` VALUES"


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
            print("proportion of valid pages as of db line " + str(n) + ": " + str(valid_pages / total_pages))
        n += 1

        line = str(file.readline(), 'utf-8')
        if not check_valid_line(line):
            break
        pages = convert_db_line(line)
        valid_pages += count_valid(pages)
        total_pages += len(pages)
        file_size += estimate_file_size(pages)
    
    print("\ndone! final stats:")
    print("number of database data lines: " + str(n))
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

        line = str(db_file.readline(), 'utf-8')
        if not check_valid_line(line):
            break
        pages = convert_db_line(line)
        write_pages_to_file(pages, out_file)
    
    print("done! file has been written.")


def main():
    # uncomment if you'd like to get some stats on the wikipedia dataset
    # with gzip.open(PATH, "r") as file:
    #     print_stats(file, HEADER_SIZE)

    with gzip.open(PATH, "r") as db, open("pages.txt", "w") as out:
        write_db_file(db, out, HEADER_SIZE)
        

if __name__ == "__main__":
    main()