# 5ClicksToJesus

Dataset taken from [the dump of English Wikipedia taken by the Wikimedia Foundation on 2024/03/01](https://dumps.wikimedia.org/enwiki/20240301/)

We converted the original data from MySQL dumps into gzip'ed text files, and removed any data not relevant to our project.
Further, we converted all links to redirect pages found in the links table into links that go directly to the final page.

Written in Python with a Flask frontend using Jinja2 template files for the web stuff. Mostly just basic stuff to keep
our project looking pretty!

### Setup

Clone the GitHub repo, then add two files to the `datasets/` folder

1. [File 1](https://drive.google.com/file/d/13WHgstLPo9A7YO-7ZKhb-RTVvVltovBP/view?usp=sharing) should be added to `datasets/current/` and should be renamed `links.txt.gz`
2. [File 2](https://drive.google.com/file/d/18fTUxN1QeKu_ofQwan-DPeLWXJuRCi7X/view?usp=sharing) should be added to `datasets/2010/` and should also be renamed `links.txt.gz`

### Distance Breakdown
|Distance|Count|
|---|---|
|0|1|
|1|14713|
|2|1440814|
|3|5219515|
|4|131984|
|5|25|
|6+|0|
|unreachable|1165|

This means that, barring the 1165 pages that are completely disconnected from the Wikipedia link network, you can start from any page on Wikipedia and reach Jesus in 5 clicks or less!

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
