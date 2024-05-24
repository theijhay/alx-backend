#!/usr/bin/env python3
"""Hypermedia Pagination"""
import csv
import math
from typing import List, Dict


def index_range(page: int, page_size: int) -> tuple:
    """
    Returns a tuple containing the start and end indexes
    for a given page and page size.

    Args:
        page (int): The page number to retrieve (1-indexed).
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: A tuple containing the start and end
        indexes for the given page and page size.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a page of the dataset based on the provided
        page and page size.

        Args:
            page (int, optional): The page number to retrieve (1-indexed).
            Defaults to 1.
            page_size (int, optional): The number of items per page.
            Defaults to 10.

        Returns:
            List[List]: A list of lists containing the data for
            the requested page.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        dataset = self.dataset()
        start, end = index_range(page, page_size)
        page_data = dataset[start:end]

        return page_data

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        Retrieves a dictionary containing hypermedia metadata
        for the requested page.

        Args:
            page (int, optional): The page number to
            retrieve (1-indexed). Defaults to 1.
            page_size (int, optional): The number of items
            per page. Defaults to 10.

        Returns:
            Dict: A dictionary containing hypermedia metadata
            for the requested page.
        """
        data = self.get_page(page, page_size)
        total_items = len(self.dataset())
        total_pages = math.ceil(total_items / page_size)

        next_page = page + 1 if page < total_pages else None
        prev_page = page - 1 if page > 1 else None

        hypermedia = {
            "page_size": page_size,
            "page": page,
            "data": data,
            "next_page": next_page,
            "prev_page": prev_page,
            "total_pages": total_pages,
        }

        return hypermedia
