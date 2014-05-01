import sys
from apps import QuotesApp

def setup():
    quotes_app = QuotesApp('quotes/quotes.txt', './quotes/html')
    return quotes_app

def teardown():
    pass
