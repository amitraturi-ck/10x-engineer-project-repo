# PromptLab API Reference

## Overview

PromptLab is a professional prompt management platform API built with FastAPI. This document provides comprehensive documentation for all available endpoints, including request/response examples and error handling.

**Base URL**: `http://localhost:8000`

**API Version**: 1.0.0

**Authentication**: None required (open API - authentication recommended for production)

---

## Table of Contents

1. [Health & Status](#health--status)
2. [Prompts](#prompts)
   - [List Prompts](#list-prompts)
   - [Get Prompt](#get-prompt)
   - [Create Prompt](#create-prompt)
   - [Update Prompt (Full)](#update-prompt-full)
   - [Update Prompt (Partial)](#update-prompt-partial)
   - [Delete Prompt](#delete-prompt)
3. [Collections](#collections)
   - [List Collections](#list-collections)
   - [Get Collection](#get-collection)
   - [Create Collection](#create-collection)
   - [Delete Collection](#delete-collection)
4. [Error Handling](#error-handling)
5. [Data Models](#data-models)
6. [Query Parameters](#query-parameters)
7. [Best Practices](#best-practices)

---

## Health & Status

### Health Check

Verify that the API server is running and healthy.

**Endpoint**: `GET /health`

**Summary**: Check API Health

**Authentication**: Not required

#### Request

```bash
curl -X GET "http://localhost:8000/health"
```

#### Response

**Status Code**: `200 OK`

```json
{
  "status": "healthy",
  "message": "API is running normally"
}
```

#### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Health status ("healthy" or "unhealthy") |
| `message` | string | Descriptive status message |

#### Use Cases

- Load balancer health checks
- Deployment verification
- Monitoring and alerting systems

---

## Prompts

### List Prompts

Retrieve all prompts with optional filtering, searching, and sorting.

**Endpoint**: `GET /prompts`

**Summary**: List All Prompts

**Authentication**: Not required

#### Request

```bash
# Get all prompts
curl -X GET "http://localhost:8000/prompts"

# Get prompts in a specific collection (filter)
curl -X GET "http://localhost:8000/prompts?collection_id=col_12345"

# Search prompts by keyword
curl -X GET "http://localhost:8000/prompts?search=python"

# Sort oldest first
curl -X GET "http://localhost:8000/prompts?sort_by=date_asc"

# Combined: search + filter + sort
curl -X GET "http://localhost:8000/prompts?collection_id=col_12345&search=generator&sort_by=date_desc"
```

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `collection_id` | string | No | None | Filter by collection ID |
| `search` | string | No | None | Search in title and description (case-insensitive) |
| `sort_by` | string | No | `date_desc` | Sort order: `date_desc` (newest first) or `date_asc` (oldest first) |

#### Response

**Status Code**: `200 OK`

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Python Code Generator",
    "content": "Write clean, well-documented Python code that accomplishes the following task:\n\n{{task}}\n\nUse best practices including type hints, docstrings, and error handling.",
    "description": "Generates high-quality Python code with best practices",
    "collection_id": "col_python_123",
    "created_at": "2026-02-20T14:30:00",
    "updated_at": "2026-02-27T10:15:00"
  },
  {
    "id": "650e8400-e29b-41d4-a716-446655440001",
    "title": "API Documentation Writer",
    "content": "Create comprehensive API documentation for the following endpoint:\n\n{{endpoint_description}}\n\nInclude request/response examples and error scenarios.",
    "description": "Helps write professional API documentation",
    "collection_id": "col_api_456",
    "created_at": "2026-02-18T10:00:00",
    "updated_at": "2026-02-25T16:45:00"
  }
]
```

#### Response Schema

Returns an array of Prompt objects. Each prompt contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique prompt identifier |
| `title` | string | Prompt title |
| `content` | string | Prompt content/instructions |
| `description` | string \| null | Optional description |
| `collection_id` | string \| null | Associated collection ID |
| `created_at` | string (ISO8601) | Creation timestamp |
| `updated_at` | string (ISO8601) | Last update timestamp |

#### Examples

**Example 1: Get all prompts**

```bash
curl -X GET "http://localhost:8000/prompts"
```

```json
[
  { "id": "abc123", "title": "Code Generator", ... },
  { "id": "def456", "title": "Documentation Writer", ... }
]
```

**Example 2: Filter by collection**

```bash
curl -X GET "http://localhost:8000/prompts?collection_id=python_prompts"
```

```json
[
  { "id": "abc123", "title": "Python Code Generator", "collection_id": "python_prompts", ... }
]
```

**Example 3: Search prompts**

```bash
curl -X GET "http://localhost:8000/prompts?search=code"
```

```json
[
  { "id": "abc123", "title": "Code Generator", ... },
  { "id": "xyz789", "title": "Code Review Helper", ... }
]
```

**Example 4: Combined filtering**

```bash
curl -X GET "http://localhost:8000/prompts?collection_id=python_prompts&search=generator&sort_by=date_desc"
```

---

### Get Prompt

Retrieve a specific prompt by its unique identifier.

**Endpoint**: `GET /prompts/{prompt_id}`

**Summary**: Get a Single Prompt

**Authentication**: Not required

#### Request

```bash
curl -X GET "http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000"
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | string | Yes | The unique identifier of the prompt |

#### Response

**Status Code**: `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Python Code Generator",
  "content": "Write clean, well-documented Python code that accomplishes the following task:\n\n{{task}}\n\nUse best practices including type hints, docstrings, and error handling.",
  "description": "Generates high-quality Python code with best practices",
  "collection_id": "col_python_123",
  "created_at": "2026-02-20T14:30:00",
  "updated_at": "2026-02-27T10:15:00"
}
```

#### Error Responses

**Status Code**: `404 Not Found`

```json
{
  "detail": "Prompt not found"
}
```

#### Use Cases

- Display prompt details in UI
- Retrieve prompt for editing
- Fetch prompt for AI model inference

---

### Create Prompt

Create a new prompt in the system.

**Endpoint**: `POST /prompts`

**Summary**: Create a New Prompt

**Authentication**: Not required

**Content-Type**: `application/json`

#### Request

```bash
curl -X POST "http://localhost:8000/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Code Review Helper",
    "content": "Review the following code and provide constructive feedback:\n\n{{code}}\n\nFocus on: readability, performance, security, and best practices.",
    "description": "Analyzes code and suggests improvements",
    "collection_id": "col_code_review"
  }'
```

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Prompt title (any length) |
| `content` | string | Yes | Prompt content (minimum 10 characters) |
| `description` | string | No | Optional description of the prompt |
| `collection_id` | string | No | ID of collection to organize prompt |

#### Response

**Status Code**: `201 Created`

```json
{
  "id": "760e8400-e29b-41d4-a716-446655440002",
  "title": "Code Review Helper",
  "content": "Review the following code and provide constructive feedback:\n\n{{code}}\n\nFocus on: readability, performance, security, and best practices.",
  "description": "Analyzes code and suggests improvements",
  "collection_id": "col_code_review",
  "created_at": "2026-02-27T12:00:00",
  "updated_at": "2026-02-27T12:00:00"
}
```

#### Error Responses

**Status Code**: `400 Bad Request` - Invalid content

```json
{
  "detail": "Prompt content must be at least 10 characters long"
}
```

#### Example Requests

**Example 1: Minimal prompt creation**

```bash
curl -X POST "http://localhost:8000/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Simple Prompt",
    "content": "This is a test prompt with enough characters"
  }'
```

**Example 2: Complete prompt with collection**

```bash
curl -X POST "http://localhost:8000/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "JavaScript Code Generator",
    "content": "Write clean JavaScript code that: {{requirements}}\n\nUse modern ES6+ syntax and include error handling.",
    "description": "Generates production-ready JavaScript",
    "collection_id": "javascript_prompts"
  }'
```

**Example 3: Template prompt with variables**

```bash
curl -X POST "http://localhost:8000/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Documentation Generator",
    "content": "Generate {{doc_type}} documentation for:\n\nProject: {{project_name}}\nPurpose: {{purpose}}\nAudience: {{audience}}\n\nInclude examples and usage guidelines.",
    "description": "Creates comprehensive documentation",
    "collection_id": "documentation"
  }'
```

---

### Update Prompt (Full)

Perform a full update on an existing prompt. All provided fields are updated; omitted fields are unchanged.

**Endpoint**: `PUT /prompts/{prompt_id}`

**Summary**: Update Entire Prompt

**Authentication**: Not required

**Content-Type**: `application/json`

#### Request

```bash
curl -X PUT "http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Python Code Generator",
    "content": "Write optimized Python code for: {{task}}\n\nInclude type hints and comprehensive error handling.",
    "description": "Updated description",
    "collection_id": "python_v2"
  }'
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | string | Yes | The unique identifier of the prompt to update |

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | No | Updated prompt title |
| `content` | string | No | Updated prompt content |
| `description` | string | No | Updated description |
| `collection_id` | string | No | Updated collection ID |

#### Response

**Status Code**: `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated Python Code Generator",
  "content": "Write optimized Python code for: {{task}}\n\nInclude type hints and comprehensive error handling.",
  "description": "Updated description",
  "collection_id": "python_v2",
  "created_at": "2026-02-20T14:30:00",
  "updated_at": "2026-02-27T13:45:00"
}
```

**Note**: The `updated_at` timestamp is automatically set to the current time.

#### Error Responses

**Status Code**: `404 Not Found`

```json
{
  "detail": "Prompt not found"
}
```

#### Use Cases

- Update prompt after testing refinements
- Move prompt to different collection
- Fix typos or improve wording

---

### Update Prompt (Partial)

Perform a partial update on an existing prompt. Only provided fields are updated; omitted fields remain unchanged.

**Endpoint**: `PATCH /prompts/{prompt_id}`

**Summary**: Partially Update Prompt

**Authentication**: Not required

**Content-Type**: `application/json`

#### Request

```bash
# Update only title
curl -X PATCH "http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Title Only"
  }'

# Update only description
curl -X PATCH "http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description"
  }'

# Update content and collection
curl -X PATCH "http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "New content here",
    "collection_id": "new_collection"
  }'
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | string | Yes | The unique identifier of the prompt to update |

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | No | New title (if updating) |
| `content` | string | No | New content (if updating) |
| `description` | string | No | New description (if updating) |
| `collection_id` | string | No | New collection ID (if updating) |

#### Response

**Status Code**: `200 OK`

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "New Title Only",
  "content": "Write clean, well-documented Python code that accomplishes the following task:\n\n{{task}}\n\nUse best practices including type hints, docstrings, and error handling.",
  "description": "Generates high-quality Python code with best practices",
  "collection_id": "col_python_123",
  "created_at": "2026-02-20T14:30:00",
  "updated_at": "2026-02-27T14:00:00"
}
```

**Note**: The `updated_at` timestamp is automatically set to the current time.

#### Error Responses

**Status Code**: `404 Not Found`

```json
{
  "detail": "Prompt not found"
}
```

#### Difference: PATCH vs PUT

| Aspect | PATCH | PUT |
|--------|-------|-----|
| **Fields** | Only provided fields updated | All fields specified are updated |
| **Omitted Fields** | Remain unchanged | Not modified |
| **Use Case** | Minor updates (title, description) | Complete replacement |
| **Data Loss Risk** | Minimal | Higher if fields are omitted |

#### Use Cases

- Quick title or description fix
- Move prompt to different collection
- Minimal content refinement
- Mass updates via API (update only changed fields)

---

### Delete Prompt

Permanently delete a prompt from the system.

**Endpoint**: `DELETE /prompts/{prompt_id}`

**Summary**: Delete a Prompt

**Authentication**: Not required

#### Request

```bash
curl -X DELETE "http://localhost:8000/prompts/550e8400-e29b-41d4-a716-446655440000"
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt_id` | string | Yes | The unique identifier of the prompt to delete |

#### Response

**Status Code**: `204 No Content`

(No response body)

#### Error Responses

**Status Code**: `404 Not Found`

```json
{
  "detail": "Prompt not found"
}
```

#### Important Notes

⚠️ **Warning**: This operation is permanent and cannot be undone. The prompt is immediately removed from the system.

#### Use Cases

- Remove outdated prompts
- Clean up test/demo prompts
- Archive workflow (delete from active, export first)

---

## Collections

### List Collections

Retrieve all collections in the system.

**Endpoint**: `GET /collections`

**Summary**: List All Collections

**Authentication**: Not required

#### Request

```bash
curl -X GET "http://localhost:8000/collections"
```

#### Response

**Status Code**: `200 OK`

```json
[
  {
    "id": "col_python_123",
    "name": "Python Prompts",
    "description": "Collection of Python-related prompts and utilities",
    "created_at": "2026-02-15T08:00:00"
  },
  {
    "id": "col_api_456",
    "name": "API Documentation",
    "description": "Prompts for generating API documentation",
    "created_at": "2026-02-16T10:30:00"
  },
  {
    "id": "col_test_789",
    "name": "Testing Prompts",
    "description": "Unit tests, integration tests, and QA prompts",
    "created_at": "2026-02-17T14:15:00"
  }
]
```

#### Response Schema

Returns an array of Collection objects. Each collection contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string (UUID) | Unique collection identifier |
| `name` | string | Collection name |
| `description` | string \| null | Optional description |
| `created_at` | string (ISO8601) | Creation timestamp |

#### Use Cases

- Display collection sidebar in UI
- Get all available organization buckets
- List categories for user selection

---

### Get Collection

Retrieve a specific collection by its unique identifier.

**Endpoint**: `GET /collections/{collection_id}`

**Summary**: Get a Single Collection

**Authentication**: Not required

#### Request

```bash
curl -X GET "http://localhost:8000/collections/col_python_123"
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collection_id` | string | Yes | The unique identifier of the collection |

#### Response

**Status Code**: `200 OK`

```json
{
  "id": "col_python_123",
  "name": "Python Prompts",
  "description": "Collection of Python-related prompts and utilities",
  "created_at": "2026-02-15T08:00:00"
}
```

#### Error Responses

**Status Code**: `404 Not Found`

```json
{
  "detail": "Collection not found"
}
```

#### Use Cases

- Get collection details for display
- Verify collection exists before adding prompts
- Fetch collection metadata

---

### Create Collection

Create a new collection for organizing prompts.

**Endpoint**: `POST /collections`

**Summary**: Create a New Collection

**Authentication**: Not required

**Content-Type**: `application/json`

#### Request

```bash
curl -X POST "http://localhost:8000/collections" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Testing Prompts",
    "description": "Unit tests, integration tests, and QA prompts"
  }'
```

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Collection name (any length) |
| `description` | string | No | Optional collection description |

#### Response

**Status Code**: `201 Created`

```json
{
  "id": "col_test_789",
  "name": "Testing Prompts",
  "description": "Unit tests, integration tests, and QA prompts",
  "created_at": "2026-02-27T15:30:00"
}
```

#### Example Requests

**Example 1: Minimal collection**

```bash
curl -X POST "http://localhost:8000/collections" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Quick Collection"
  }'
```

**Example 2: Collection with description**

```bash
curl -X POST "http://localhost:8000/collections" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "JavaScript Prompts",
    "description": "React, Node.js, and frontend prompts"
  }'
```

#### Use Cases

- Create new project/team organization
- Set up category for prompts
- Organize by programming language
- Organize by use case (testing, docs, etc.)

---

### Delete Collection

Delete a collection from the system.

**Endpoint**: `DELETE /collections/{collection_id}`

**Summary**: Delete a Collection

**Authentication**: Not required

#### Request

```bash
curl -X DELETE "http://localhost:8000/collections/col_python_123"
```

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `collection_id` | string | Yes | The unique identifier of the collection to delete |

#### Response

**Status Code**: `204 No Content`

(No response body)

#### Error Responses

**Status Code**: `404 Not Found`

```json
{
  "detail": "Collection not found"
}
```

**Status Code**: `409 Conflict` - Collection contains prompts

```json
{
  "detail": "Cannot delete collection with existing prompts"
}
```

#### Important Notes

⚠️ **Data Integrity**: A collection cannot be deleted if it contains prompts. This prevents orphaned prompts. To delete a collection:

1. Delete or reassign all prompts in the collection, OR
2. Move prompts to a different collection

#### Example Workflow

```bash
# Get prompts in collection
curl -X GET "http://localhost:8000/prompts?collection_id=col_python_123"

# Move prompts to another collection
curl -X PATCH "http://localhost:8000/prompts/{prompt_id}" \
  -H "Content-Type: application/json" \
  -d '{"collection_id": "col_backup"}'

# Delete empty collection
curl -X DELETE "http://localhost:8000/collections/col_python_123"
```

#### Use Cases

- Remove deprecated project/team organization
- Clean up unused categories
- Reorganize structure

---

## Error Handling

### HTTP Status Codes

The API uses standard HTTP status codes to indicate the result of an API request.

| Code | Name | Description |
|------|------|-------------|
| `200` | OK | Request successful |
| `201` | Created | Resource successfully created |
| `204` | No Content | Request successful (no content to return) |
| `400` | Bad Request | Invalid request data or parameters |
| `404` | Not Found | Resource does not exist |
| `409` | Conflict | Request conflicts with current state |
| `500` | Internal Server Error | Server error |

### Error Response Format

All error responses follow this standard format:

```json
{
  "detail": "Human-readable error message describing what went wrong"
}
```

### Common Error Scenarios

#### Invalid Prompt Content (400)

```bash
curl -X POST "http://localhost:8000/prompts" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Too Short",
    "content": "short"
  }'
```

**Response:**

```json
{
  "detail": "Prompt content must be at least 10 characters long"
}
```

#### Prompt Not Found (404)

```bash
curl -X GET "http://localhost:8000/prompts/invalid_id_12345"
```

**Response:**

```json
{
  "detail": "Prompt not found"
}
```

#### Collection Delete with Prompts (409)

```bash
curl -X DELETE "http://localhost:8000/collections/col_has_prompts"
```

**Response:**

```json
{
  "detail": "Cannot delete collection with existing prompts"
}
```

#### Empty Search Query (400)

```bash
curl -X GET "http://localhost:8000/prompts?search="
```

**Response:**

```json
{
  "detail": "Search query cannot be empty"
}
```

### Handling Errors in Code

**JavaScript/Fetch Example:**

```javascript
fetch('/prompts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Test',
    content: 'short'
  })
})
.then(response => {
  if (!response.ok) {
    return response.json().then(error => {
      throw new Error(`Error ${response.status}: ${error.detail}`);
    });
  }
  return response.json();
})
.catch(error => console.error('Request failed:', error.message));
```

**Python/Requests Example:**

```python
import requests

try:
    response = requests.post(
        'http://localhost:8000/prompts',
        json={
            'title': 'Test',
            'content': 'short'
        }
    )
    response.raise_for_status()
    prompt = response.json()
except requests.exceptions.HTTPError as e:
    error_detail = e.response.json().get('detail', 'Unknown error')
    print(f"Error {e.response.status_code}: {error_detail}")
```

---

## Data Models

### Prompt Model

Complete structure of a Prompt object.

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Python Code Generator",
  "content": "Write clean, well-documented Python code that accomplishes the following task:\n\n{{task}}\n\nUse best practices including type hints, docstrings, and error handling.",
  "description": "Generates high-quality Python code with best practices",
  "collection_id": "col_python_123",
  "created_at": "2026-02-20T14:30:00",
  "updated_at": "2026-02-27T10:15:00"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string (UUID) | Always | Auto-generated unique identifier |
| `title` | string | Always | Descriptive title for the prompt |
| `content` | string | Always | Main prompt text/instructions (min 10 chars) |
| `description` | string \| null | Optional | Detailed explanation of prompt purpose |
| `collection_id` | string \| null | Optional | ID of organizing collection |
| `created_at` | string (ISO8601) | Always | UTC timestamp of creation |
| `updated_at` | string (ISO8601) | Always | UTC timestamp of last modification |

### Collection Model

Complete structure of a Collection object.

```json
{
  "id": "col_python_123",
  "name": "Python Prompts",
  "description": "Collection of Python-related prompts and utilities",
  "created_at": "2026-02-15T08:00:00"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string (UUID) | Always | Auto-generated unique identifier |
| `name` | string | Always | Human-readable collection name |
| `description` | string \| null | Optional | Purpose and details of collection |
| `created_at` | string (ISO8601) | Always | UTC timestamp of creation |

### Health Response Model

```json
{
  "status": "healthy",
  "message": "API is running normally"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Status indicator ("healthy" or "unhealthy") |
| `message` | string | Descriptive status message |

---

## Query Parameters

### Common Query Parameters

#### Collection ID Filter

Used with: `GET /prompts`

```bash
curl -X GET "http://localhost:8000/prompts?collection_id=col_python_123"
```

Returns only prompts in the specified collection.

#### Search Query

Used with: `GET /prompts`

```bash
curl -X GET "http://localhost:8000/prompts?search=code+generator"
```

Performs case-insensitive full-text search in prompt title and description.

**Search Features:**
- Case-insensitive matching
- Searches both title and description
- Partial matches supported (substring matching)
- Requires non-empty query

#### Sort By

Used with: `GET /prompts`

```bash
# Newest first (default)
curl -X GET "http://localhost:8000/prompts?sort_by=date_desc"

# Oldest first
curl -X GET "http://localhost:8000/prompts?sort_by=date_asc"
```

**Valid Values:**
- `date_desc` (default) - Sort by creation date, newest first
- `date_asc` - Sort by creation date, oldest first

---

## Best Practices

### 1. API Usage

- **Always include Content-Type header** for POST/PUT/PATCH requests:
  ```bash
  -H "Content-Type: application/json"
  ```

- **Check status codes** before processing response:
  ```javascript
  if (response.status === 201) {
    // Handle success
  } else if (response.status === 400 || response.status === 404) {
    // Handle error
  }
  ```

- **Use appropriate HTTP methods**:
  - `GET` - Retrieve data (no side effects)
  - `POST` - Create new resource
  - `PUT` - Full update/replace
  - `PATCH` - Partial update (preferred for minor changes)
  - `DELETE` - Remove resource

### 2. Prompt Design

- **Use template variables** for dynamic content:
  ```
  {{variable_name}}
  ```

- **Keep content above 10 characters** (validation requirement)

- **Use meaningful titles** for easy searching and organization

- **Add descriptions** for clarity on prompt purpose

- **Organize with collections** for better management

### 3. Error Handling

- **Always handle potential 404 errors** when fetching by ID

- **Validate response status** before parsing JSON

- **Check for 409 Conflict** when deleting collections

- **Implement retry logic** for 500 errors (with exponential backoff)

### 4. Performance

- **Filter/search on server** rather than client side
- **Use pagination** for large result sets (future feature)
- **Cache GET responses** when appropriate
- **Reuse connections** with persistent HTTP clients

### 5. Security (Production Recommendations)

- **Authentication**: Implement API key or OAuth2 authentication
- **Rate limiting**: Prevent abuse with request rate limits
- **Input validation**: Additional client-side validation
- **CORS**: Restrict allowed origins (currently `*` for development)
- **HTTPS**: Use HTTPS in production (not HTTP)
- **Audit logging**: Track all API modifications

### 6. Integration Examples

**Create a Prompt and Assign to Collection:**

```bash
# 1. Create collection
COLLECTION=$(curl -s -X POST "http://localhost:8000/collections" \
  -H "Content-Type: application/json" \
  -d '{"name":"Python","description":"Python prompts"}' \
  | jq -r '.id')

# 2. Create prompt in collection
curl -X POST "http://localhost:8000/prompts" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\":\"Code Generator\",
    \"content\":\"Write Python code for {{task}}\",
    \"collection_id\":\"$COLLECTION\"
  }"
```

**Search and Retrieve:**

```bash
# 1. Search for prompts
PROMPT_ID=$(curl -s "http://localhost:8000/prompts?search=generator" \
  | jq -r '.[0].id')

# 2. Get full details
curl -X GET "http://localhost:8000/prompts/$PROMPT_ID"
```

**Update and Move to Different Collection:**

```bash
# 1. Create new collection
NEW_COL=$(curl -s -X POST "http://localhost:8000/collections" \
  -H "Content-Type: application/json" \
  -d '{"name":"Archive"}' \
  | jq -r '.id')

# 2. Move prompt (partial update)
curl -X PATCH "http://localhost:8000/prompts/{prompt_id}" \
  -H "Content-Type: application/json" \
  -d "{\"collection_id\":\"$NEW_COL\"}"
```

---

## Appendix: Full cURL Examples

### Complete CRUD Workflow

```bash
#!/bin/bash
set -e

BASE_URL="http://localhost:8000"
CONTENT_TYPE="Content-Type: application/json"

echo "=== Create Collection ==="
COLLECTION=$(curl -s -X POST "$BASE_URL/collections" \
  -H "$CONTENT_TYPE" \
  -d '{"name":"Demo","description":"Demo collection"}' \
  | jq -r '.id')
echo "Created collection: $COLLECTION"

echo -e "\n=== Create Prompt ==="
PROMPT=$(curl -s -X POST "$BASE_URL/prompts" \
  -H "$CONTENT_TYPE" \
  -d "{
    \"title\":\"Demo Prompt\",
    \"content\":\"This is a demo prompt with enough characters\",
    \"description\":\"A test prompt\",
    \"collection_id\":\"$COLLECTION\"
  }" \
  | jq -r '.id')
echo "Created prompt: $PROMPT"

echo -e "\n=== Retrieve Prompt ==="
curl -s -X GET "$BASE_URL/prompts/$PROMPT" | jq '.'

echo -e "\n=== Update Prompt (PATCH) ==="
curl -s -X PATCH "$BASE_URL/prompts/$PROMPT" \
  -H "$CONTENT_TYPE" \
  -d '{"title":"Updated Demo Prompt"}' | jq '.title'

echo -e "\n=== List Prompts in Collection ==="
curl -s -X GET "$BASE_URL/prompts?collection_id=$COLLECTION" | jq 'length'

echo -e "\n=== Delete Prompt ==="
curl -s -X DELETE "$BASE_URL/prompts/$PROMPT"
echo "Deleted prompt"

echo -e "\n=== Delete Collection ==="
curl -s -X DELETE "$BASE_URL/collections/$COLLECTION"
echo "Deleted collection"

echo -e "\n=== Verify Deletion (404) ==="
curl -s -X GET "$BASE_URL/prompts/$PROMPT" | jq '.detail'
```

---

## Support & Questions

For issues or questions:

1. Check the [README.md](../README.md) for setup instructions
2. Review [Swagger UI](http://localhost:8000/docs) for interactive API testing
3. Check error messages in the `detail` field
4. Review status codes and error handling section above

---

**Last Updated**: February 27, 2026  
**API Version**: 1.0.0  
**Framework**: FastAPI 0.109.0