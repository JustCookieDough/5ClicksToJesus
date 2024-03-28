
import gzip, os
from build_link_dataset import make_db as make_link_db
from build_page_dataset import make_ns0_dict, make_db as make_page_db
from build_redirect_dict import make_redirect_dict

PAGES_PATH = "enwiki-20240301-page.sql.gz"
LINKS_PATH = "enwiki-20240301-pagelinks.sql.gz"
REDIRECTS_PATH = "enwiki-20240301-redirect.sql.gz"

PAGES_HEADER_SIZE = 50
LINKS_HEADER_SIZE = 43
REDIRECTS_HEADER_SIZE = 40

def main():
    # clear the display
    os.system('cls' if os.name == 'nt' else 'clear')

    # print some nice ascii art!
    print("  _      __   _    __     _      __                    \n | | /| / /  (_)  / /__  (_) ___/ / __ __  __ _    ___ \n | |/ |/ /  / /  /  '_/ / / / _  / / // / /  ' \\  / _ \\\n |__/|__/  /_/  /_/\\_\\ /_/  \\_,_/  \\_,_/ /_/_/_/ / .__/\n                                                /_/    \n   ___         __                   __                 \n  / _ \\ ___ _ / /_ ___ _  ___ ___  / /_                \n / // // _ `// __// _ `/ (_-</ -_)/ __/                \n/____/ \\_,_/ \\__/ \\_,_/ /___/\\__/ \\__/                 \n                                                       \n   ___          _    __     __                         \n  / _ ) __ __  (_)  / / ___/ / ___   ____              \n / _  |/ // / / /  / / / _  / / -_) / __/              \n/____/ \\_,_/ /_/  /_/  \\_,_/  \\__/ /_/                 \n")
    print("- scott, alex, max, and ming")

    # begin!
    print("starting database making! this is gonna take a while, so grab some tea/coffee and chillax!\n")
    
    # page db
    print("making page database...")
    with gzip.open(PAGES_PATH, "r") as db, open("pages.txt", "w") as out:
        make_page_db(db, out, PAGES_HEADER_SIZE)
    print("done!\n")
    
    # ns0 dict
    print("making dictionary of page names/ids in namespace 0...")
    with gzip.open(PAGES_PATH, "r") as db:
        ns0 = make_ns0_dict(db, PAGES_HEADER_SIZE)
    print("done!\n")

    # rd dict
    print("making a dictionary of redirect pages...")
    with gzip.open(REDIRECTS_PATH, "r") as db:
        rd = make_redirect_dict(db, ns0, REDIRECTS_HEADER_SIZE)
    print("done!\n")

    # line db
    print("making line database... (this takes forever, so settle in)")
    with gzip.open(LINKS_PATH, "r") as db, open("links.txt", "w") as out:
        make_link_db(db, out, ns0, rd, LINKS_HEADER_SIZE)
    print("done!\n")

    print("all done! enjoy your databases! (i recommend compressing them with gzip -9 for space reasons)") # yay, done!

if __name__ == "__main__":
    main()