
import re
from io import FileIO

def check_valid_block(block: str) -> bool:
    return block[:29] == "INSERT INTO `redirect` VALUES"

def make_rd_dict_block(block: str, ns0: dict[str, int]) -> dict[int, int]:
    out_dict = {}
    page_strings = block[31:-3].split("),(")
    p = re.compile("(\d+),([\d-]+),'(.+?)',")
    for page_string in page_strings:
        r = p.search(page_string)
        try:
            if r.group(3) in ns0:            # target page in ns0 (and also exists lmao)
                out_dict[int(r.group(1))] = ns0[r.group(3)]
        except:
            pass

    return out_dict

def make_redirect_dict(db_file: FileIO, ns0: dict[str, int], header_size: int) -> dict[int, int]:
    for i in range(header_size):
        db_file.readline()

    out_dict = {}
    while True:

        block = str(db_file.readline(), 'utf-8')
        if not check_valid_block(block):
            break
        block_dict = make_rd_dict_block(block, ns0)
        out_dict.update(block_dict)

    return out_dict