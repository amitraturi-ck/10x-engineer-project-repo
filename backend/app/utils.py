"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort a list of Prompt objects by their creation timestamp.

    Args:
        prompts: A list of Prompt objects to sort.
        descending: If True, sort newest first (default). If False, sort oldest first.

    Returns:
        A new list of Prompt objects sorted by their created_at attribute.

    Example:
        >>> sorted_prompts = sort_prompts_by_date(prompts, descending=True)
        >>> print(sorted_prompts[0].created_at)
    """
    # BUG #3 FIX: Now respects the 'descending' parameter
    # Sorts in descending order (newest first) by default
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Return prompts that belong to a specific collection.

    Args:
        prompts: A list of Prompt objects to filter.
        collection_id: The identifier of the collection to match.

    Returns:
        A list of Prompt objects whose collection_id equals the provided collection_id.

    Example:
        >>> user_prompts = filter_prompts_by_collection(all_prompts, "collection-123")
        >>> len(user_prompts)
        5
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Search prompts by title or description, case-insensitive.

    Args:
        prompts: A list of Prompt objects to search.
        query: The search query string. Matches against title and description.

    Returns:
        A list of Prompt objects where the query appears in the title or description.

    Example:
        >>> results = search_prompts(prompts, "email")
        >>> for r in results:
        ...     print(r.title)
    """
    query_lower = query.lower()
    return [
        p for p in prompts
        if query_lower in p.title.lower() or
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Validate prompt content meets basic non-empty and length requirements.

    A valid prompt should:
    - Not be empty
    - Not be just whitespace
    - Be at least 10 characters (after trimming)

    Args:
        content: The prompt content string to validate.

    Returns:
        True if the content is valid, False otherwise.

    Example:
        >>> validate_prompt_content("  Short  ")
        False
        >>> validate_prompt_content("Write an email to a client.")
        True
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract template variable names from prompt content.

    Variables are expected in the format {{variable_name}} and will return the
    variable_name parts as strings.

    Args:
        content: The prompt content containing template variables.

    Returns:
        A list of variable names (strings) found in the content. Returns an empty
        list if no variables are present.

    Example:
        >>> extract_variables("Hello, {{first_name}} {{last_name}}!")
        ['first_name', 'last_name']
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)
