"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection,PromptVersion


class Storage:
    """A simple in-memory storage container for prompts and collections.

    This class provides CRUD-style operations for Prompt and Collection objects
    stored in memory. It is intended for testing and development; persistence
    is not durable across process restarts.

    Example:
        >>> s = Storage()
        >>> p = Prompt(id="p1", title="T", content="C", created_at=0, collection_id="c1")
        >>> s.create_prompt(p)
        >>> s.get_prompt("p1").title
        'T'
    """
    def __init__(self):
        """Initialize empty in-memory stores for prompts and collections."""
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
        self._versions: Dict[str, List[PromptVersion]] = {}

    # ============== Prompt Operations ==============

    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Store a Prompt object and return it.

        If a prompt with the same id already exists it will be overwritten.

        Args:
            prompt: The Prompt instance to store.

        Returns:
            The stored Prompt instance.

        Example:
            >>> p = Prompt(id="p2", title="Hi", content="Body", created_at=1, collection_id="c1")
            >>> storage.create_prompt(p).id
            'p2'
        """
        self._prompts[prompt.id] = prompt
        return prompt

    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by its unique identifier.

        Args:
            prompt_id: The unique identifier of the prompt to retrieve.

        Returns:
            The Prompt object if found, otherwise None.

        Example:
            >>> storage.get_prompt("p2").title
            'Hi'
        """
        return self._prompts.get(prompt_id)

    def get_all_prompts(self) -> List[Prompt]:
        """Return a list of all stored Prompt objects.

        Returns:
            A list containing all Prompt instances currently stored.

        Example:
            >>> len(storage.get_all_prompts())  # returns number of prompts stored
            1
        """
        return list(self._prompts.values())

    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Update an existing prompt by id.

        If the prompt_id does not exist, None is returned.

        Args:
            prompt_id: The id of the prompt to update.
            prompt: The new Prompt instance to store under prompt_id.

        Returns:
            The updated Prompt if the id existed, otherwise None.

        Example:
            >>> updated = storage.update_prompt("p2", p)
            >>> updated.id
            'p2'
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    # ============== Versioning Operations ==============

    def add_version(self, prompt: Prompt) -> None:
        """Save a snapshot of the prompt before it is modified."""
        versions = self._versions.setdefault(prompt.id, [])

        version = PromptVersion(
            prompt_id=prompt.id,
            version=len(versions) + 1,
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            collection_id=prompt.collection_id,
            created_at=prompt.created_at,
        )

        versions.append(version)

    def get_versions(self, prompt_id: str) -> List[PromptVersion]:
        """Return all saved versions for a prompt."""
        return self._versions.get(prompt_id, [])

    def delete_prompt(self, prompt_id: str) -> bool:
        """Delete a prompt by id.

        Args:
            prompt_id: The id of the prompt to delete.

        Returns:
            True if a prompt was deleted, False if no prompt with the id existed.

        Example:
            >>> storage.delete_prompt("p2")
            True
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False

    # ============== Collection Operations ==============

    def create_collection(self, collection: Collection) -> Collection:
        """Store a Collection object and return it.

        If a collection with the same id already exists it will be overwritten.

        Args:
            collection: The Collection instance to store.

        Returns:
            The stored Collection instance.

        Example:
            >>> c = Collection(id="c1", name="Default")
            >>> storage.create_collection(c).id
            'c1'
        """
        self._collections[collection.id] = collection
        return collection

    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Retrieve a collection by its unique identifier.

        Args:
            collection_id: The unique identifier of the collection to retrieve.

        Returns:
            The Collection object if found, otherwise None.

        Example:
            >>> storage.get_collection("c1").name
            'Default'
        """
        return self._collections.get(collection_id)

    def get_all_collections(self) -> List[Collection]:
        """Return a list of all stored Collection objects.

        Returns:
            A list containing all Collection instances currently stored.

        Example:
            >>> len(storage.get_all_collections())
            1
        """
        return list(self._collections.values())

    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection by id.

        Args:
            collection_id: The id of the collection to delete.

        Returns:
            True if a collection was deleted, False if no collection with the id existed.

        Example:
            >>> storage.delete_collection("c1")
            True
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False

    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """Return prompts that belong to a specific collection.

        Args:
            collection_id: The identifier of the collection to match.

        Returns:
            A list of Prompt objects whose collection_id equals the provided collection_id.

        Example:
            >>> storage.get_prompts_by_collection("c1")
            [<Prompt ...>]
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]

    # ============== Utility ==============

    def clear(self):
        """Remove all stored prompts and collections.

        This will empty both the prompts and collections stores.

        Example:
            >>> storage.clear()
            >>> storage.get_all_prompts()
            []
        """
        self._prompts.clear()
        self._collections.clear()
        self._versions.clear()


# Global storage instance
storage = Storage()
