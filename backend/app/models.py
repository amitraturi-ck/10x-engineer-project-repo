"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List,Dict
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a unique identifier using UUID4.

    Returns:
        str: A unique UUID4 string.
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Get the current UTC datetime.

    Returns:
        datetime: Current datetime in UTC timezone.
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Base Pydantic model for Prompt data.

    This model contains the core fields shared across prompt creation,
    updates, and responses. It defines the structure for prompt data
    without database-specific fields like id or timestamps.

    Attributes:
        title (str): The name or title of the prompt. Must be a non-empty string.
        content (str): The actual prompt content/text. Should contain the prompt
            engineering instructions or template.
        description (Optional[str]): Optional detailed description of the prompt's
            purpose and use case. Defaults to None.
        collection_id (Optional[str]): Optional identifier linking this prompt to
            a collection. Used to organize related prompts. Defaults to None.
    """
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Pydantic model for creating a new Prompt.

    Inherits all fields from PromptBase and is used to validate
    incoming POST request payloads for prompt creation.
    """
    pass


class PromptUpdate(PromptBase):
    """Pydantic model for updating an existing Prompt.

    All fields are optional to support partial updates (PATCH requests).
    Only provided fields will be updated; missing fields are ignored.

    Attributes:
        title (Optional[str]): Updated title if provided. Defaults to None.
        content (Optional[str]): Updated content if provided. Defaults to None.
        description (Optional[str]): Updated description if provided. Defaults to None.
        collection_id (Optional[str]): Updated collection association if provided.
            Defaults to None.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None
    pass


class Prompt(PromptBase):
    """Pydantic model representing a complete Prompt with metadata.

    This model includes all PromptBase fields plus database-specific
    metadata (id and timestamps). Used in API responses to represent
    the full state of a prompt in the system.

    Attributes:
        id (str): Unique identifier for the prompt. Generated as UUID4.
        created_at (datetime): Timestamp when the prompt was created in UTC.
        updated_at (datetime): Timestamp when the prompt was last modified in UTC.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Base Pydantic model for Collection data.

    Contains the core fields shared across collection operations.
    Defines the essential structure for a collection without
    database-specific fields.

    Attributes:
        name (str): The display name of the collection. Must be non-empty.
        description (Optional[str]): Optional description explaining the
            collection's purpose and contents. Defaults to None.
    """
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Pydantic model for creating a new Collection.

    Inherits all fields from CollectionBase and is used to validate
    incoming POST request payloads for collection creation.
    """
    pass


class Collection(CollectionBase):
    """Pydantic model representing a complete Collection with metadata.

    This model includes all CollectionBase fields plus the collection's
    unique identifier and creation timestamp. Used in API responses to
    represent the full state of a collection in the system.

    Attributes:
        id (str): Unique identifier for the collection. Generated as UUID4.
        created_at (datetime): Timestamp when the collection was created in UTC.
    """
    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Pydantic model for listing prompts with pagination metadata.

    This model wraps a list of prompts with total count information,
    typically used in API responses for GET /prompts endpoints to provide
    both the prompt data and metadata about the full result set.

    Attributes:
        prompts (List[Prompt]): List of Prompt objects returned from the query.
            Each prompt contains full metadata (id, timestamps, etc).
        total (int): Total count of prompts matching the query criteria.
            Useful for pagination and showing result counts to users.
    """
    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Pydantic model for listing collections with pagination metadata.

    This model wraps a list of collections with total count information,
    typically used in API responses for GET /collections endpoints to provide
    both the collection data and metadata about the full result set.

    Attributes:
        collections (List[Collection]): List of Collection objects returned
            from the query. Each collection contains full metadata (id, timestamps).
        total (int): Total count of collections in the system.
            Useful for pagination and showing collection counts to users.
    """
    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Pydantic model for API health check response.

    This model represents the response from the health check endpoint,
    providing basic information about the API's operational status and version.
    Typically used by monitoring systems and load balancers to verify
    that the API is running and responsive.

    Attributes:
        status (str): The operational status of the API. Common values include
            "healthy", "ok", or similar indicators. Used to determine if the
            service is ready to handle requests.
        version (str): The current version of the API software. Helps clients
            identify which version they are communicating with.
    """
    status: str
    version: str
class PromptVersion(BaseModel):
    prompt_id: str
    version: int
    title: str
    content: str
    description: Optional[str]
    collection_id: Optional[str]
    created_at: datetime
    archived_at: datetime = Field(default_factory=get_current_time)
class PromptVersionList(BaseModel):
    prompt_id: str
    versions: List[PromptVersion]

class PromptRunRequest(BaseModel):
    variables: Optional[Dict[str, str]] = Field(default_factory=dict)

class PromptRunResponse(BaseModel):
    result: str
