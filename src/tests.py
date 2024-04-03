"""
Description: Testing functions to test compliance with PyTA and doctests
Date: 2024-04-01
Authors: Maxwell Antao Zhang, Yin Ming Chan, Alex Lewis, Scott Angelides
"""
import doctest
import python_ta
import python_ta.contracts


def run_tests() -> None:
    """
    Runs tests! PyTA and friends!
    """
    python_ta.contracts.check_all_contracts()

    doctest.testmod()

    python_ta.check_all(["search.py", "app.py", "tests.py"], config={
        'extra-imports': ['os', 'flask', 'search', 'tests', 'gzip', 'io'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120,
        'disable': ["C9103", "E9992", "E9997", "E9998"]  # disabling the "code at module level, etc."" warnings that we
    })                                                   # get from our flask stuff. okay'd by prof. sharmin!
