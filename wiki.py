#!/usr/bin/python

import argparse
import concurrent.futures
import threading

import wikipedia
from rich import print, pretty
from rich.columns import Columns
from rich.panel import Panel
from rich.pretty import Pretty

pretty.install()
thread_local = threading.local()


# sub-command functions
def search(args):
    kwards = args._get_kwargs()
    search_query = kwards.__getitem__(0).__getitem__(1)
    is_all = kwards.__getitem__(1).__getitem__(1)

    results = get_search_results(search_query, display_all=is_all)

    print('There what we found:')
    print(results)


def open_page(args):
    page_title = args._get_kwargs().__getitem__(0).__getitem__(1)
    print('Page:', page_title)

    result = wikipedia.page(title=page_title)
    print(result)


# utility functions
def get_search_results(search_query, display_all=False):
    pages = wikipedia.search(search_query)

    if display_all:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(get_page_summary, page) for page in pages]

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
