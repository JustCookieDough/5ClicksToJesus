# 5ClicksToJesus

Dataset taken from [the dump of English Wikipedia taken by the Wikimedia Foundation on 2024/03/01](https://dumps.wikimedia.org/enwiki/20240301/)

We converted the original data from MySQL dumps into gzip'ed CSV files, and removed any data not relevant to our project.
Further, we converted all links to redirect pages found in the links table into links that go directly to the final page.

Written in Python with a Flask frontend using Jinja2 template files for the web stuff. Mostly just basic stuff to keep
our project looking pretty!

### Some pages to try out:
- Basic Test Cases
    - United Kingdom  (close)
    - Harry Potter  (medium)
    - Methane  (far)
    - Jesus  (distance 0)
    - [not found atm]  (not connected)
- Special Charcters
    - Sid Meier's Pirates!  (single quote)
    - Barack Obama "Joker" poster  (double quote)
    - \o/  (backslash)
- More cool test cases to come!