#!/usr/bin/env python3
"""Simple Helper Function"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns a tuple containing the start and end indexes for a
    given page and page size.

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
