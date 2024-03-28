# TODO: write this lmao

import gzip
import re
from io import FileIO
from page_dataset_builder import make_redirect_set, make_ns0_dict

PATH = "enwiki-20240301-pagelinks.sql.gz"
PAGES_PATH = "enwiki-20240301-page.sql.gz"
HEADER_SIZE = 42

class Link():
    start: int
    end: int

    def __init__(self, start_id: int, end_id: int):
        self.start = start_id
        self.end = end_id


def check_valid_block(block: str) -> bool:
    return block[:30] == "INSERT INTO `pagelinks` VALUES"


def load_page_to_id_dataset(path: str) -> dict[str, int]:
    page_ds_file = gzip.open(path, "r")
    out_dict = {}

    while True:
        line = str(page_ds_file.readline(), 'utf-8').strip()
        if line == "":
            break
        data = line.split(" ")
        try:
            out_dict[data[1]] = data[0]
        except:
            print(line, data)

    return out_dict


def make_rd_dict_block(block: str, ns0: dict[str, int], rd: set) -> dict[int, int]:
    out_dict = {}
    page_strings = block[32:-3].split("),(")
    p = re.compile("(\d+),(\d+),'(.+?)',(\d+),")
    for page_string in page_strings:
        r = p.search(page_string)
        try:
            if (int(r.group(2)) == 0            # target page in ns0
              and int(r.group(4)) == 0          # source page in ns0
              and r.group(3) in ns0             # target page exists
              and int(r.group(1)) in rd):       # source page a redirect
                out_dict[int(r.group(1))] = ns0[r.group(3)]
        except:
            print('fuck shit page conversion broke, heres the page string')
            print(page_string)

    return out_dict


def make_rd_dict(db_file: FileIO, ns0: dict[str, int], rd: set, header_size: int) -> dict[int, int]:
    
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
        block_dict = create_rd_dict_block(block, ns0, rd)
        out_dict.update(block_dict)

    return out_dict


def convert_db_block(block: str, ns0: dict[str, int], rd: dict[int, int]) -> list[Link]:
    out_list = []
    page_strings = block[32:-3].split("),(")
    p = re.compile("(\d+),(\d+),'(.+?)',(\d+),")
    for page_string in page_strings:
        r = p.search(page_string)
        try:
            if (int(r.group(2)) == 0            # target page in ns0
              and int(r.group(4)) == 0          # source page in ns0
              and r.group(3) in ns0             # target page exists
              and int(r.group(1)) not in rd):   # source page not a redirect
                if ns0[r.group(3)] in rd:       # if target page is a redirect
                    out_list.append(Link(
                        int(r.group(1)),
                        rd[ns0[r.group(3)]]     # convert the target to the redirect's target
                    ))
                else:
                    out_list.append(Link(
                        int(r.group(1)),
                        ns0[r.group(3)]
                    ))
        except:
            print('fuck shit page conversion broke, heres the page string')
            print(page_string)

    return out_list


def main():
    with gzip.open(PAGES_PATH, "r") as db:
        ns0 = make_ns0_dict(db, 50)
    
    with gzip.open(PAGES_PATH, "r") as db:
        rd = make_redirect_set(db, 50)

    with gzip.open(PATH, "r") as db:
        rd_dict = make_rd_dict(db, ns0, rd, 42)

    print(rd_dict[12])


if __name__ == "__main__":
    main()