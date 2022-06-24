#!/usr/bin/python

import argparse
import wikipedia
import time
import threading
import concurrent.futures

from rich.columns import Columns
from rich import print, pretty
from rich.pretty import Pretty
from rich.panel import Panel
from rich.progress import track
from rich.progress import Progress

pretty.install()
thread_local = threading.local()

# sub-command functions
def search(args):
    kwards = args._get_kwargs()
    search_quary = kwards.__getitem__(0).__getitem__(1)
    isAll = kwards.__getitem__(1).__getitem__(1)

    results = get_search_results(search_quary, display_All=isAll)

    print('There what we found:')
    print(results)

def open_page(args):
    page_title = args._get_kwargs().__getitem__(0).__getitem__(1)
    print('Page:', page_title)

    result = wikipedia.page(title=page_title)
    print(result)

# utility functions
def get_search_results(search_quary, display_All=False):
    pages = wikipedia.search(search_quary)

    if display_All:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(get_page_summary, page) for page in pages]
        
        print('все ок')
        
        pages_renderables = [Panel(f.result()) for f in concurrent.futures.as_completed(futures)]

    else:
        pages_renderables = [Pretty(page) for page in pages]
    return Columns(pages_renderables)

def get_page_summary(page):
    title = page
    summary = wikipedia.summary(page, sentences=1)
    return f"[b]{title}[/b]\n[yellow]{summary}"


# create the top-level parser
parser = argparse.ArgumentParser(description='Access to Wikipedia via the command line')
subparsers = parser.add_subparsers()

# create the parser for the "search" command
parser_search = subparsers.add_parser('search', help='search help')
parser_search.add_argument('Search_query', type=str)
parser_search.add_argument('--all', action='store_const', const=True, default=False)
parser_search.set_defaults(func=search)

# create the parser for the "open" command
parser_search = subparsers.add_parser('open', help='open help')
parser_search.add_argument('Page title', type=str)
parser_search.set_defaults(func=open_page)

args = parser.parse_args()
args.func(args)
