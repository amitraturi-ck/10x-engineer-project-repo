"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from app.models import (
    Prompt, PromptCreate, PromptUpdate,
    Collection, CollectionCreate,
    PromptList, CollectionList, HealthResponse,PromptVersionList,
    get_current_time
)
from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Return basic health information about the API.

    Args:
        None

    Returns:
        HealthResponse: Object containing status and version of the API.

    Raises:
        None

    Example:
        >>> resp = health_check()
        >>> resp.status
        "ok"
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """Retrieve a list of prompts with optional filtering, search, and sorting.

    Args:
        collection_id (Optional[str]): If provided, only prompts in this
            collection are returned.
        search (Optional[str]): Full-text search applied to title and description.
        sort (Optional[str]): Sorting order, e.g. "asc" or "desc" (by created_at).

    Returns:
        PromptList: Wrapper containing list of matching Prompt objects and total count.

    Raises:
        None

    Example:
        >>> res = list_prompts(collection_id="c1", search="todo", sort="desc")
        >>> print(res.total)
        5
    """
    prompts = storage.get_all_prompts()

    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)

    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)

    # Sort by date (newest first)
    # Note: There might be an issue with the sorting...
    prompts = sort_prompts_by_date(prompts, descending=True)

    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a prompt by its unique identifier.

    Args:
        prompt_id (str): The unique identifier of the prompt to retrieve.

    Returns:
        Prompt: The Prompt object if found.

    Raises:
        HTTPException: 404 if the prompt is not found.
        ValueError: If prompt_id is empty or invalid format.

    Example:
        >>> prompt = get_prompt("abc123")
        >>> print(prompt.title)
        "My Prompt"
    """

    # FIX #1: Validate prompt_id is not empty or null
    # Return 404 if prompt_id is invalid
    if not prompt_id or not prompt_id.strip():
        raise HTTPException(status_code=404, detail="Prompt not found")

    # Check if prompt exists before accessing attributes
    # Return 404 if not found instead of causing 500 error
    prompt = storage.get_prompt(prompt_id.strip())
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@app.get("/prompts/{prompt_id}/versions", response_model=PromptVersionList)
def get_prompt_versions(prompt_id: str):
    """Return version history for a prompt."""

    if not prompt_id or not prompt_id.strip():
        raise HTTPException(status_code=404, detail="Prompt not found")

    prompt = storage.get_prompt(prompt_id.strip())
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    versions = storage.get_versions(prompt_id.strip())

    return PromptVersionList(prompt_id=prompt_id.strip(), versions=versions)

@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt.

    Args:
        prompt (PromptCreate): Payload describing the prompt to create.

    Returns:
        Prompt: The newly created Prompt with id and timestamps.

    Raises:
        HTTPException: 400 if the referenced collection does not exist or validation fails.

    Example:
        >>> new = create_prompt(PromptCreate(title="X", content="..."))
        >>> print(new.id)
        "uuid-..."
    """

    # Validate collection exists if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Replace an existing prompt with the provided data.

    Args:
        prompt_id (str): Identifier of the prompt to replace.
        prompt (PromptCreate): New prompt data (all required fields).

    Returns:
        Prompt: The updated Prompt object.

    Raises:
        HTTPException: 404 if the prompt does not exist.
        HTTPException: 400 if the referenced collection does not exist.

    Example:
        >>> updated = update_prompt("abc123", PromptCreate(...))
        >>> print(updated.updated_at)
        datetime(...)
    """

    # Validate prompt_data is not null
    if not prompt_data:
        raise HTTPException(status_code=400, detail="Invalid request data")

    # Validate prompt_id is not empty or null
    if not prompt_id or not prompt_id.strip():
        raise HTTPException(status_code=404, detail="Prompt not found")

    existing = storage.get_prompt(prompt_id.strip())
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    storage.add_version(existing)
    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # FIX #2: Update the updated_at timestamp to current time
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()  # FIX: Now uses current time instead of old timestamp
    )

    return storage.update_prompt(prompt_id.strip(), updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Partially update an existing prompt.

    Args:
        prompt_id (str): Identifier of the prompt to modify.
        prompt (PromptUpdate): Payload with fields to update (partial).

    Returns:
        Prompt: The prompt after applying updates.

    Raises:
        HTTPException: 404 if the prompt does not exist.
        HTTPException: 400 if a provided collection_id does not exist.

    Example:
        >>> patched = patch_prompt("abc123", PromptUpdate(title="New"))
        >>> print(patched.title)
        "New"
    """
    # Validate prompt_id is not empty or null
    if not prompt_id or not prompt_id.strip():
        raise HTTPException(status_code=404, detail="Prompt not found")

    existing = storage.get_prompt(prompt_id.strip())
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    storage.add_version(existing)

    # Validate collection if provided
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    # Partial update: only update provided fields
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title if prompt_data.title is not None else existing.title,
        content=prompt_data.content if prompt_data.content is not None else existing.content,
        description=prompt_data.description if prompt_data.description is not None else existing.description,
        collection_id=prompt_data.collection_id if prompt_data.collection_id is not None else existing.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id.strip(), updated_prompt)


@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Delete a prompt by its identifier.

    Args:
        prompt_id (str): Identifier of the prompt to delete.

    Returns:
        None

    Raises:
        HTTPException: 404 if the prompt does not exist.

    Example:
        >>> delete_prompt("abc123")
    """
    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None # pragma: no cover


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """List all collections.

    Args:
        None

    Returns:
        CollectionList: Wrapper containing list of Collection objects and total count.

    Raises:
        None

    Example:
        >>> cols = list_collections()
        >>> print(cols.total)
        3
    """
    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a collection by its unique identifier.

    Args:
        collection_id (str): The unique identifier of the collection to retrieve.

    Returns:
        Collection: The Collection object if found.

    Raises:
        HTTPException: 404 if the collection is not found.

    Example:
        >>> col = get_collection("col-123")
        >>> print(col.name)
        "Examples"
    """
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Create a new collection.

    Args:
        collection (CollectionCreate): Payload describing the collection to create.

    Returns:
        Collection: The newly created Collection with id and created_at.

    Raises:
        HTTPException: 400 if validation fails.

    Example:
        >>> c = create_collection(CollectionCreate(name="New"))
        >>> print(c.id)
        "uuid-..."
    """
    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection if it has no associated prompts.

    Args:
        collection_id (str): Identifier of the collection to delete.

    Returns:
        None

    Raises:
        HTTPException: 404 if the collection does not exist.
        HTTPException: 400 if the collection still contains prompts.

    Example:
        >>> delete_collection("col-123")
    """
    # Check if collection_id is null, empty, or blank after trimming
    if not collection_id or not collection_id.strip():
        raise HTTPException(status_code=400, detail="Invalid collection ID")

    # Check if collection exists
    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    # Check if collection has associated prompts
    all_prompts = storage.get_all_prompts()
    prompts_in_collection = filter_prompts_by_collection(all_prompts, collection_id)

    if prompts_in_collection:
        raise HTTPException(status_code=400, detail="Collection is associated with existing prompts")

    # Delete collection if it has no prompts
    storage.delete_collection(collection_id)
    return None
