
import re
from io import FileIO
from datatypes import Link


def check_valid_block(block: str) -> bool:
    return block[:30] == "INSERT INTO `pagelinks` VALUES"

def make_db_block(block: str, ns0: dict[str, int], rd: dict[int, int]) -> list[Link]:
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
            pass
    return out_list

def make_db(db_file: FileIO, out_file: FileIO, ns0: dict[str, int], rd: set, header_size: int) -> None:
    for i in range(header_size):
        db_file.readline()

    while True:
        block = str(db_file.readline(), 'utf-8')
        if not check_valid_block(block):
            break
        links = make_db_block(block, ns0, rd)
        for link in links:
            out_file.write(f"{link.start} {link.end}\n")