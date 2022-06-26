#!/usr/bin/python

import argparse
import concurrent.futures
import asyncio

import wikipedia
from rich import print, pretty
from rich.columns import Columns
from rich.panel import Panel
from rich.pretty import Pretty
from rich.progress import Progress

pretty.install()


# sub-command functions
async def search(args):
    with Progress(transient=True) as progress:
        task = progress.add_task(f"[cyan]Searching {args.Search_query}...", total=None, start=False)
        result = await get_search_results(args.Search_query, all_items=args.all, with_summary=args.with_summary)
        while not result:
            progress.update(task)

    print('[b]There what we found:[/b]')
    search_results = result.__getitem__(0)
    all_results_length = result.__getitem__(1)
    display_results_length = result.__getitem__(2)

    print(search_results)

    if all_results_length > display_results_length:
        print(f"And also {all_results_length - display_results_length} more results.")
        print(f"Run the [b]search[/b] command with the [b]--all[/b] attribute to view all search results")


async def open_page(args):
    with Progress(transient=True) as progress:
        task = progress.add_task(f"[cyan]Opening {args.Page_title}...", total=None, start=False)
        await asyncio.sleep(1)

        if (args.whole_page):
            wiki_page = wikipedia.page(args.Page_title)
        else:
            wiki_page = wikipedia.summary(args.Page_title, sentences=5)

        while not wiki_page:
            progress.update(task)

    if (args.whole_page):
        result = Panel(f"[yellow][b]{wiki_page.title}[/b][/yellow]\n" +
                       f"[b]Link: {wiki_page.url}[/b]\n\n" +
                       wiki_page.content)
    else:
        result = Panel(wiki_page)

    print(result)


# utility functions
async def get_search_results(search_query, with_summary=False, all_items=False):
    pages = wikipedia.search(search_query)
    all_results_length = len(pages)
    display_results_length = len(pages)

    if not all_items:
        pages = pages[:5]
        display_results_length = 5

    if with_summary:

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(get_page_summary, page) for page in pages]
            await asyncio.sleep(1)

        pages_renderables = Columns(Panel(f.result()) for f in concurrent.futures.as_completed(futures))

    else:
        pages_renderables = Columns([Pretty(page) for page in pages])

    return pages_renderables, all_results_length, display_results_length


def get_page_summary(page_title):
    summary = wikipedia.summary(page_title, sentences=1)
    return f"[yellow]{page_title}[/yellow]\n{summary}"


# create the top-level parser
parser = argparse.ArgumentParser(description='Access to Wikipedia via the command line')
subparsers = parser.add_subparsers()

# create the parser for the "search" command
parser_search = subparsers.add_parser('search', help='search {title} {options}.')
parser_search.add_argument('Search_query', type=str)
parser_search.add_argument('-s',
                           action='store_const',
                           const=True, default=False,
                           dest='with_summary',
                           help='Display search results with summary')
parser_search.add_argument('--with-summary',
                           action='store_const',
                           const=True, default=False,
                           dest='with_summary',
                           help='Display search results with summary')
parser_search.add_argument('-a',
                           action='store_const',
                           const=True, default=False,
                           dest='all',
                           help='Display all search results')
parser_search.add_argument('--all',
                           action='store_const',
                           const=True, default=False,
                           dest='all',
                           help='Display all search results')
parser_search.set_defaults(func=search)

# create the parser for the "open" command
parser_open = subparsers.add_parser('open', help='open {title} {options}.')
parser_open.add_argument('Page_title', type=str)
parser_open.add_argument('-w',
                           action='store_const',
                           const=True, default=False,
                           dest='whole_page',
                           help='Display whole page')
parser_open.add_argument('--whole',
                           action='store_const',
                           const=True, default=False,
                           dest='whole_page',
                           help='Display whole page')
parser_open.set_defaults(func=open_page)

args = parser.parse_args()
asyncio.run(args.func(args))
