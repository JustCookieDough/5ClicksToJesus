# 5ClicksToJesus

Dataset taken from [the dump of English Wikipedia taken by the Wikimedia Foundation on 2024/03/01](https://dumps.wikimedia.org/enwiki/20240301/)

We converted the original data from MySQL dumps into gzip'ed CSV files, and removed any data not relevant to our project.
Further, we converted all links to redirect pages found in the links table into links that go directly to the final page.

Written in Python with a Flask frontend using Jinja2 template files for the web stuff. Mostly just basic stuff to keep
our project looking pretty!

### Some pages to try out:
- Basic Test Cases
    - Jesus                               (distance 0)
    - Harry Potter                        (distance 1)
    - Methane                             (distance 2)
    - Stardew Valley                      (distance 3)
    - Inter frame                         (distance 4)
    - Buccaneer Bay (radio play)          (distance 5)
    - Curtiss H                           (not connected)

- Special Charcters
    - Sid Meier's Pirates!  (single quote)
    - Barack Obama "Joker" poster  (double quote)
    - \o/  (backslash)
    
- Every Distance 5 Wikipedia Page:
    - Federation of Manufacturing Opticians
    - USS Bonito
    - Caspar CLE 16
    - Centre for Indian Christian Archaeological Research
    - IEC 61010
    - Digital nerve
    - Buccaneer Bay (radio play)
    - Zabnik
    - Home Care Insight
    - Marow
    - Khen (DJ)
    - Gisvan
    - Haruhisa Soda
    - Golam Kabud
    - Qovaq
    - Operating capacity
    - Ribosomal rescue factor
    - Feng Wu
    - Sawsan Abd-Elrahman Hakim
    - MOS:EM
    - Liu Ching
    - Socket FMx
    - Alaa Fouad
    - Australian Stages
    - 栄町駅