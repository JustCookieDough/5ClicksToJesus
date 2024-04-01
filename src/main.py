"""
Description: Use a graph to represent the links between wikipedia pages to in order to calculate
the shortest path to Jesus from any given page.
Date: 2024-04-01
Authors: Maxwell Antao Zhang, Yin Ming Chan, Alex Lewis, Scott Angelides
"""
from app import App

app = App("links.txt.gz", "pages.txt.gz")
app.run()
