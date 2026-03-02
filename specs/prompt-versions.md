# Feature Specification: Prompt Version History & Management

**Document Version**: 1.0
**Status**: Ready for Implementation (Week 3)
**Last Updated**: February 27, 2026
**Priority**: High
**Complexity**: Medium

---

## 1. Overview

### 1.1 Feature Description

The Prompt Version History feature enables users to track, compare, and restore previous versions of prompts. This feature maintains a complete audit trail of all prompt modifications, allowing users to:

- View the complete history of changes to any prompt
- Compare different versions side-by-side
- Restore previous versions with one click
- Understand who changed what and when (for future auth implementation)
- Track version metadata (author, change description, timestamp)

### 1.2 Motivation & Business Value

**Problem Solved:**
- Users accidentally overwrite prompts without recovery option
- No way to compare prompt evolution
- Loss of context about when/why prompts were changed
- Difficult to maintain prompt quality standards without audit trail

**Business Benefits:**
- ✅ Increased user confidence (safety net for experimentation)
- ✅ Better prompt governance (track changes)
- ✅ Learning tool (see what works/doesn't work)
- ✅ Compliance ready (audit trail for enterprises)
- ✅ Competitive advantage (industry standard feature)

### 1.3 Success Metrics

| Metric | Target | Definition |
|--------|--------|-----------|
| **User Adoption** | 60%+ | % of users who restore a version |
| **Restore Success Rate** | 99%+ | Successful restores / attempted restores |
| **Version Creation** | 1M+/month | Total versions created across platform |
| **Query Performance** | <100ms | 99th percentile latency for version list |
| **Storage Efficiency** | <2x | Total storage vs baseline |

### 1.4 Scope & Timeline

**Scope:**
- ✅ Version creation on every prompt modification
- ✅ Version history viewing
- ✅ Version comparison (side-by-side)
- ✅ Version restoration (manual restore operation)
- ✅ Version metadata (timestamps, summaries)

**Out of Scope (Future):**
- ❌ Automatic version cleanup/retention policies
- ❌ Branching/merging versions
- ❌ Version comments/annotations
- ❌ Collaborative merging

**Timeline:** Week 3 (2-3 days implementation, 1 day testing)

---

## 2. User Stories & Acceptance Criteria

### Story 1: View Version History

**As a** prompt creator
**I want to** view a complete list of all versions of a prompt
**So that** I can track how the prompt has evolved over time

#### Acceptance Criteria

```gherkin
Given a prompt with multiple modifications
When I request the version history
Then I receive a list of all versions in reverse chronological order
  And each version includes:
    ✓ Version ID (unique identifier)
    ✓ Version number (1, 2, 3, ...)
    ✓ Created timestamp (ISO8601)
    ✓ Summary of changes (optional)
    ✓ Content preview (first 200 chars)
    ✓ Content hash (for integrity)
    ✓ Author (placeholder for future auth)
  And most recent version is marked as "current"
  And pagination works for 100+ versions

When I filter by date range
Then only versions within range are returned

When I search version summaries
Then matching versions are highlighted
```

#### Implementation Notes

- **API Endpoint**: `GET /prompts/{id}/versions`
- **Response**: `VersionListResponse` (paginated)
- **Pagination**: 20 versions per page
- **Query Parameters**: `page`, `limit`, `search`, `sort`

---

### Story 2: Compare Two Versions

**As a** prompt creator
**I want to** compare two different versions side-by-side
**So that** I can understand what changed between them

#### Acceptance Criteria

```gherkin
Given two versions of a prompt
When I request a comparison
Then I see a side-by-side diff view showing:
    ✓ Title changes (highlighted)
    ✓ Content changes (highlighted with +/- indicators)
    ✓ Description changes (highlighted)
    ✓ Collection changes (if applicable)
    ✓ Metadata comparison (timestamps, etc.)
  And unchanged fields show as identical
  And additions are marked in green (+)
  And deletions are marked in red (-)
  And the diff is readable and scrollable

When I compare with the current version
Then current version is clearly labeled as "Current"

When I compare non-consecutive versions (e.g., v1 vs v5)
Then the comparison still works correctly
```

#### Implementation Notes

- **API Endpoint**: `GET /prompts/{id}/versions/{v1_id}/compare/{v2_id}`
- **Response**: `VersionComparison` (detailed diff)
- **Diff Algorithm**: Unified diff format (similar to git)
- **Performance**: <500ms for comparison

**Diff Example:**

```diff
Title
- Old Title
+ New Title

Content
  Write clean Python code for: {{task}}
- Use best practices including type hints
+ Use best practices including:
+   - Type hints
+   - Docstrings
+   - Error handling

Description
- Generates Python code
+ Generates high-quality Python code with best practices
```

---

### Story 3: Restore a Previous Version

**As a** prompt creator
**I want to** restore a prompt to a previous version
**So that** I can undo unwanted changes

#### Acceptance Criteria

```gherkin
Given a historical version of a prompt
When I request restoration
Then the system creates a new version with restored content
  And the restored version:
    ✓ Contains exact copy of historical version content
    ✓ Gets a new version ID
    ✓ Gets current timestamp
    ✓ Includes summary: "Restored from version X"
    ✓ Is marked as current version
    ✓ Updates the prompt's updated_at timestamp
  And the historical version remains unchanged

When I restore to the current version
Then an error is returned: "Cannot restore to current version"

When restoration succeeds
Then I receive the restored prompt with confirmation

When restoration fails (prompt deleted)
Then I receive clear error: "Cannot restore: prompt no longer exists"

When I restore a version multiple times
Then distinct versions are created for each restore
```

#### Implementation Notes

- **API Endpoint**: `POST /prompts/{id}/versions/{version_id}/restore`
- **Response**: `Prompt` (restored prompt object)
- **Operation**: Atomic transaction
- **Idempotent**: No (creates new version each time)
- **Status Code**: 201 Created

**Request Body:**
```json
{
  "summary": "Restoring to cleaner version"  // Optional
}
```

**Response:**
```json
{
  "id": "prompt-123",
  "title": "Original Title",
  "content": "Original content...",
  "current_version_id": "version-789",
  "version_number": 8,
  "restored": true
}
```

---

### Story 4: Automatic Version Creation on Save

**As a** system
**I want to** automatically create a version whenever a prompt is modified
**So that** all changes are automatically tracked

#### Acceptance Criteria

```gherkin
When a prompt is created (POST /prompts)
Then version 1 is automatically created

When a prompt is updated (PUT /prompts/{id})
Then a new version is created with incremented version_number

When a prompt is partially updated (PATCH /prompts/{id})
Then a new version is created (same as PUT)

When multiple fields are updated simultaneously
Then one version is created (not one per field)

When a prompt is restored
Then a new version with "restored" flag is created

When version creation fails
Then the update operation is rolled back
  And the user receives clear error
  And the original prompt remains unchanged

When the system creates >1000 versions for one prompt
Then performance remains acceptable (<100ms lookup)
```

#### Implementation Notes

- **Trigger**: On every `PUT` and `PATCH` operation
- **Storage**: Separate `versions` table/collection
- **Cleanup**: No automatic deletion (retention policy future feature)
- **Atomicity**: Version creation must succeed with update or both fail
- **Performance**: Version creation overhead <50ms

---

### Story 5: Version Metadata & Audit Trail

**As a** system administrator
**I want to** track detailed metadata for each version
**So that** I can maintain audit compliance and understand change patterns

#### Acceptance Criteria

```gherkin
For each version stored
Then the system tracks:
    ✓ Version ID (unique)
    ✓ Version number (sequential per prompt)
    ✓ Prompt ID (which prompt this version is for)
    ✓ Full content snapshot
    ✓ Created timestamp (UTC, ISO8601)
    ✓ Author ID (placeholder: "system" or user_id)
    ✓ User agent / client info (optional)
    ✓ Change summary (optional, user-provided)
    ✓ Is current flag (only one per prompt)
    ✓ Content hash (SHA256 for deduplication)
    ✓ Size bytes (storage tracking)

When retrieving version metadata
Then sensitive fields are excluded:
    - Raw user IP addresses
    - Internal database IDs

When querying versions for an audit report
Then all versions are returned with complete metadata
```

#### Implementation Notes

- **Storage**: Denormalized version snapshots (full content copy)
- **Hash**: `hashlib.sha256(content.encode()).hexdigest()`
- **Size Tracking**: `len(content.encode('utf-8')) / 1024  # KB`

---

## 3. Data Model Changes

### 3.1 Database Schema

#### New Table: `prompt_versions`

```sql
CREATE TABLE prompt_versions (
  -- Identity
  id TEXT PRIMARY KEY,              -- UUID4
  prompt_id TEXT NOT NULL,          -- Foreign key to prompts
  version_number INTEGER NOT NULL,  -- Sequential: 1, 2, 3...

  -- Content Snapshot
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  description TEXT,
  collection_id TEXT,

  -- Metadata
  created_at TIMESTAMP NOT NULL,    -- When version was created
  author_id TEXT DEFAULT 'system',  -- User who made change (future)
  change_summary TEXT,              -- Optional user description

  -- Integrity & Analysis
  content_hash TEXT,                -- SHA256(content)
  content_size_bytes INTEGER,       -- Size tracking

  -- Flags
  is_current BOOLEAN DEFAULT FALSE, -- Only one TRUE per prompt
  is_restored BOOLEAN DEFAULT FALSE,-- Indicates restore operation

  -- Uniqueness Constraints
  UNIQUE(prompt_id, version_number),
  FOREIGN KEY(prompt_id) REFERENCES prompts(id) ON DELETE CASCADE,
  INDEX idx_prompt_versions_created (prompt_id, created_at DESC),
  INDEX idx_prompt_versions_current (prompt_id, is_current)
);
```

#### Modified Table: `prompts`

```sql
ALTER TABLE prompts ADD COLUMN (
  current_version_id TEXT,           -- Link to current version
  version_count INTEGER DEFAULT 1,   -- Total versions of this prompt
  FOREIGN KEY(current_version_id) REFERENCES prompt_versions(id)
);
```

### 3.2 Pydantic Models (Python)

```python
# Version inquiry models
class VersionMetadata(BaseModel):
    """Metadata about a specific version."""
    id: str
    version_number: int
    created_at: datetime
    author_id: str = "system"
    change_summary: Optional[str] = None
    is_current: bool = False
    is_restored: bool = False
    content_preview: str  # First 200 chars
    content_hash: str
    content_size_bytes: int


class PromptVersion(BaseModel):
    """Complete version snapshot."""
    # Metadata
    id: str
    version_number: int
    prompt_id: str
    created_at: datetime
    author_id: str = "system"
    change_summary: Optional[str] = None
    is_current: bool = False
    is_restored: bool = False

    # Full Content
    title: str
    content: str
    description: Optional[str] = None
    collection_id: Optional[str] = None

    # Integrity
    content_hash: str
    content_size_bytes: int


class VersionListResponse(BaseModel):
    """Response for listing versions."""
    versions: List[VersionMetadata]
    total: int
    page: int
    limit: int
    pages: int


class VersionComparison(BaseModel):
    """Comparison between two versions."""
    version1_id: str
    version1_number: int
    version2_id: str
    version2_number: int

    # Field diffs
    title_changed: bool
    title_diff: Optional[str] = None

    content_changed: bool
    content_diff: Optional[str] = None  # Unified diff format

    description_changed: bool
    description_diff: Optional[str] = None

    collection_changed: bool
    collection_old: Optional[str] = None
    collection_new: Optional[str] = None

    metadata: Dict[str, Any]


class VersionRestoreRequest(BaseModel):
    """Request to restore a version."""
    summary: Optional[str] = None  # User-provided context

    @validator('summary')
    def summary_length(cls, v):
        if v and len(v) > 500:
            raise ValueError('Summary must be ≤500 characters')
        return v
```

### 3.3 In-Memory Storage Adaptation

For Week 1-2 (before database migration):

```python
# In Storage class
class Storage:
    def __init__(self):
        self.prompts: Dict[str, Prompt] = {}
        self.collections: Dict[str, Collection] = {}
        self.prompt_versions: Dict[str, PromptVersion] = {}  # NEW
        self.version_index: Dict[str, List[str]] = {}  # prompt_id -> version_ids
```

---

## 4. API Endpoint Specifications

### 4.1 New Endpoints

#### Endpoint 1: List Versions (Paginated)

```http
GET /prompts/{prompt_id}/versions
```

**Purpose**: Retrieve version history for a specific prompt

**Authentication**: None (future: require auth)

**Path Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt_id` | string | Yes | ID of the prompt |

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | integer | 1 | Page number (1-indexed) |
| `limit` | integer | 20 | Versions per page (max 100) |
| `sort` | string | `date_desc` | Sort order: `date_desc`, `date_asc`, `version_desc`, `version_asc` |
| `search` | string | (none) | Search in change_summary (case-insensitive) |

**Request Example:**

```bash
curl -X GET "http://localhost:8000/prompts/prompt-123/versions?page=1&limit=20&sort=date_desc"
```

**Response: 200 OK**

```json
{
  "versions": [
    {
      "id": "version-789",
      "version_number": 5,
      "created_at": "2026-02-27T14:30:00",
      "author_id": "system",
      "change_summary": "Fixed typo in instructions",
      "is_current": true,
      "is_restored": false,
      "content_preview": "Write clean Python code for: {{task}}...",
      "content_hash": "abc123def456...",
      "content_size_bytes": 1256
    },
    {
      "id": "version-788",
      "version_number": 4,
      "created_at": "2026-02-27T13:15:00",
      "author_id": "system",
      "change_summary": null,
      "is_current": false,
      "is_restored": false,
      "content_preview": "Write Python code for: {{task}}...",
      "content_hash": "xyz789abc123...",
      "content_size_bytes": 1200
    },
    {
      "id": "version-787",
      "version_number": 3,
      "created_at": "2026-02-27T10:45:00",
      "author_id": "system",
      "change_summary": "Added error handling details",
      "is_current": false,
      "is_restored": false,
      "content_preview": "Write Python code...",
      "content_hash": "def456abc123...",
      "content_size_bytes": 1050
    }
  ],
  "total": 5,
  "page": 1,
  "limit": 20,
  "pages": 1
}
```

**Error Responses:**

| Status | Scenario | Response |
|--------|----------|----------|
| 404 | Prompt not found | `{"detail": "Prompt not found"}` |
| 400 | Invalid page/limit | `{"detail": "Page must be ≥1"}` |
| 400 | Limit exceeds max | `{"detail": "Limit must be ≤100"}` |

---

#### Endpoint 2: Get Specific Version

```http
GET /prompts/{prompt_id}/versions/{version_id}
```

**Purpose**: Retrieve full content of a specific version

**Path Parameters:**
| Param | Type | Required |
|-------|------|----------|
| `prompt_id` | string | Yes |
| `version_id` | string | Yes |

**Response: 200 OK**

```json
{
  "id": "version-789",
  "version_number": 5,
  "prompt_id": "prompt-123",
  "created_at": "2026-02-27T14:30:00",
  "author_id": "system",
  "change_summary": "Fixed typo in instructions",
  "is_current": true,
  "is_restored": false,
  "title": "Python Code Generator",
  "content": "Write clean, well-documented Python code that accomplishes: {{task}}\n\nUse best practices including:\n- Type hints\n- Docstrings\n- Error handling",
  "description": "Generates high-quality Python code",
  "collection_id": "col_python_123",
  "content_hash": "abc123def456...",
  "content_size_bytes": 1256
}
```

**Error Responses:**

| Status | Scenario |
|--------|----------|
| 404 | Prompt not found |
| 404 | Version not found |

---

#### Endpoint 3: Compare Two Versions

```http
GET /prompts/{prompt_id}/versions/{version_id_1}/compare/{version_id_2}
```

**Purpose**: Compare two versions side-by-side with diff

**Path Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt_id` | string | Yes | Prompt ID (for validation) |
| `version_id_1` | string | Yes | First version (base for comparison) |
| `version_id_2` | string | Yes | Second version (compared to base) |

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `format` | string | `unified` | Diff format: `unified` (standard), `side_by_side` |
| `context_lines` | integer | 3 | Lines of context around changes |

**Request Example:**

```bash
curl -X GET "http://localhost:8000/prompts/prompt-123/versions/version-787/compare/version-789?format=unified"
```

**Response: 200 OK**

```json
{
  "version1_id": "version-787",
  "version1_number": 3,
  "version2_id": "version-789",
  "version2_number": 5,
  "title_changed": false,
  "title_diff": null,
  "content_changed": true,
  "content_diff": "--- Version 3\n+++ Version 5\n@@ -1,5 +1,8 @@\n Write clean, well-documented Python code that accomplishes: {{task}}\n \n Use best practices including:\n+- Type hints\n+- Docstrings\n+- Error handling",
  "description_changed": true,
  "description_diff": "--- Version 3\n+++ Version 5\n@@ -1 +1 @@\n-Generates Python code\n+Generates high-quality Python code",
  "collection_changed": false,
  "collection_old": null,
  "collection_new": null,
  "metadata": {
    "lines_added": 3,
    "lines_removed": 1,
    "similarity_score": 0.95
  }
}
```

**Side-by-Side Format (Alternative):**

Request: `?format=side_by_side`

```json
{
  "title": {
    "v1": "Python Code Generator",
    "v2": "Python Code Generator",
    "changed": false
  },
  "content": {
    "v1": ["Write clean, well-documented Python code...", "Use best practices including:"],
    "v2": ["Write clean, well-documented Python code...", "Use best practices including:", "- Type hints", "- Docstrings", "- Error handling"],
    "changed": true
  }
}
```

**Error Responses:**

| Status | Scenario |
|--------|----------|
| 404 | Prompt not found |
| 404 | Version 1 not found |
| 404 | Version 2 not found |
| 400 | Versions not from same prompt |

---

#### Endpoint 4: Restore a Version

```http
POST /prompts/{prompt_id}/versions/{version_id}/restore
```

**Purpose**: Restore a prompt to a previous version

**Path Parameters:**
| Param | Type | Required |
|-------|------|----------|
| `prompt_id` | string | Yes |
| `version_id` | string | Yes |

**Request Body:**

```json
{
  "summary": "Restoring to cleaner version without deprecated fields"
}
```

**Field Validation:**
- `summary`: Optional, max 500 characters

**Request Example:**

```bash
curl -X POST "http://localhost:8000/prompts/prompt-123/versions/version-787/restore" \
  -H "Content-Type: application/json" \
  -d '{"summary": "Going back to the more concise version"}'
```

**Response: 201 Created**

```json
{
  "id": "prompt-123",
  "title": "Python Code Generator",
  "content": "Write clean Python code...",
  "description": "Generates Python code",
  "collection_id": "col_python_123",
  "created_at": "2026-02-25T10:45:00",
  "updated_at": "2026-02-27T15:00:00",
  "current_version_id": "version-790",
  "version_count": 6,
  "version_number": 6,
  "restored": true
}
```

**Error Responses:**

| Status | Scenario | Message |
|--------|----------|---------|
| 404 | Prompt not found | "Prompt not found" |
| 404 | Version not found | "Version not found" |
| 400 | Restoring to current | "Cannot restore to current version" |
| 400 | Invalid summary | "Summary must be ≤500 characters" |
| 409 | Prompt was deleted | "Cannot restore: prompt no longer exists" |

---

### 4.2 Modified Endpoints

#### POST /prompts (Create)

**Behavior Change**: Version 1 automatically created

```python
# On creation:
prompt = create_prompt(data)
version_v1 = create_version(
    prompt_id=prompt.id,
    version_number=1,
    content=prompt.content,
    # ... other fields
    is_current=True
)
prompt.current_version_id = version_v1.id
return prompt
```

---

#### PUT /prompts/{id} (Full Update)

**Behavior Change**: New version automatically created

```python
# On update:
old_prompt = get_prompt(id)
prompt = update_prompt(id, data)

new_version = create_version(
    prompt_id=id,
    version_number=prompt.version_count + 1,
    content=prompt.content,
    # ... other fields
    is_current=True
)

# Mark old current version as not current
mark_version_not_current(old_prompt.current_version_id)
prompt.current_version_id = new_version.id
prompt.version_count += 1

return prompt
```

---

#### PATCH /prompts/{id} (Partial Update)

**Behavior Change**: Same as PUT, creates new version

---

#### DELETE /prompts/{id} (Delete)

**Behavior Change**: Cascade deletes all versions

```python
# On delete:
delete_all_versions(prompt_id)
delete_prompt(prompt_id)
```

---

## 5. Edge Cases & Error Handling

### 5.1 Version Creation Edge Cases

#### Case 1: Rapid Successive Updates

**Scenario**: User makes 10 updates in 5 seconds

**Expected Behavior**:
```
Version 1: Initial creation
Version 2: Update 1 (5ms later)
Version 3: Update 2 (100ms later)
...
Version 11: Update 10 (5s later)

All versions preserved with accurate timestamps
```

**Implementation**:
- Each update = atomic transaction
- Timestamps precise to milliseconds
- No version merging or coalescing

---

#### Case 2: Concurrent Updates (Future Concern)

**Scenario**: Two users simultaneously update prompt (multi-threaded environment)

**Expected Behavior**:
```
Thread A: Read prompt v3 (time=100ms)
Thread B: Read prompt v3 (time=101ms)
Thread A: Modify and create v4 (time=150ms)
Thread B: Modify and create v5 (time=151ms)

Result: Both versions exist, no data loss
```

**Implementation**:
- Use database transactions/locks
- Atomic compare-and-swap on current_version
- Timestamp resolution down to microseconds
- Future: Implement optimistic locking

---

#### Case 3: Version Explosion

**Scenario**: Prompt auto-saved 1,000 times in one session

**Expected Behavior**:
```
All 1,000 versions stored and queryable
Pagination handles large version lists
Version operations remain <100ms latency

Future: Retention policies can prune old versions
```

**Mitigation**:
- Pagination limits results to 20-100 per request
- Indexing ensures O(log n) lookups
- Database query optimization

---

#### Case 4: Import/Bulk Operations

**Scenario**: User imports 100 templates, each gets modified 5x

**Expected Behavior**:
```
500 versions created atomically
No partial create/update scenarios
Bulk operation succeeds or completely fails
```

**Implementation**:
- Batch insert versions in single transaction
- Rollback entire batch on any failure

---

### 5.2 Comparison Edge Cases

#### Case 1: Comparing Identical Versions

**Scenario**: User compares version 3 with itself

**Expected Behavior**:
```json
{
  "title_changed": false,
  "content_changed": false,
  "description_changed": false,
  "collection_changed": false,
  "metadata": {
    "lines_added": 0,
    "lines_removed": 0,
    "similarity_score": 1.0
  }
}
```

---

#### Case 2: Very Large Diffs

**Scenario**: Comparing versions with 100KB content, major rewrites

**Expected Behavior**:
- Diff generated successfully (<500ms)
- Response compressed if >1MB
- Pagination support for large diffs (future)

---

#### Case 3: Non-Consecutive Versions

**Scenario**: Compare version 1 with version 100

**Expected Behavior**:
- Comparison shows all accumulated changes
- Works identical to comparing consecutive versions
- Query performance: O(1) lookup + O(n) diff, where n=content length

---

### 5.3 Restore Edge Cases

#### Case 1: Restore Deleted Prompt

**Scenario**: User deletes prompt, tries to restore old version

**Expected Behavior**:
```
Prompt deletion cascades to versions
Attempting to restore returns 409 Conflict
Message: "Cannot restore: prompt no longer exists"
User must manually create new prompt
```

---

#### Case 2: Restore to Current Version

**Scenario**: User clicks "Restore" on current version

**Expected Behavior**:
```
System returns 400 Bad Request
Message: "Cannot restore to current version"
No new version created
No operation side effects
```

**Implementation**:
```python
if version.is_current:
    raise HTTPException(
        status_code=400,
        detail="Cannot restore to current version"
    )
```

---

#### Case 3: Multiple Successive Restores

**Scenario**: User restores v3, then restores v1, then restores v4

**Expected Behavior**:
```
v1 creation → current_version_id points to v1, version_number=4
v2 restore from v3 → current_version_id points to new v5, version_number=5
v3 restore from v1 → current_version_id points to new v6, version_number=6
v4 restore from v4 → current_version_id points to new v7, version_number=7

Each restore creates distinct version with incremented number
Full history is preserved: 1 → 2 → 3 → 4 → 5 → 6 → 7
```

---

#### Case 4: Restore with Merged/Deleted Collections

**Scenario**: Restore version that references deleted collection

**Options**:
1. **Strict**: Reject restore with 409 (collection doesn't exist)
2. **Lenient**: Restore with collection_id=null

**Selected Approach**: Lenient (Option 2)
- Better UX (restore always succeeds)
- User can reassign collection after restore
- Prevents version restore from failing due to external changes

---

### 5.4 Data Integrity Edge Cases

#### Case 1: Hash Collision

**Scenario**: Two different prompts generate same SHA256 hash (theoretical)

**Expected Behavior**:
- Hash is informational, not durable key
- Versions identified by id, not hash
- Hash mismatch detection (future feature)

---

#### Case 2: Content Size Tracking

**Scenario**: Prompt content includes emoji, special characters, multi-byte UTF-8

**Expected Behavior**:
```python
content_size_bytes = len(content.encode('utf-8'))

"Hello" → 5 bytes
"Café" → 5 bytes (é is 2 bytes in UTF-8)
"😊" → 4 bytes (emoji is 4 bytes in UTF-8)
```

---

#### Case 3: Version Numbering in Concurrent Scenario

**Scenario**: Two updates happen simultaneously

**Expected Behavior**:
```
Both increment version_number atomically
v1 → v2 (Thread A wins race condition)
v1 → v3 (Thread B, auto-retried)

OR use optimistic locking:
Thread A successful: v1 → v2
Thread B fails with conflict error
Application retries Thread B: v2 → v3
```

---

## 6. Implementation Guidelines

### 6.1 Database Migration Strategy

**For Week 3 (transitioning from in-memory to persistent DB):**

```sql
-- Step 1: Create versions table
CREATE TABLE prompt_versions (...)

-- Step 2: Backfill existing prompts with version 1
INSERT INTO prompt_versions (id, prompt_id, version_number, ...)
SELECT uuid(), id, 1, ... FROM prompts

-- Step 3: Update prompts table
ALTER TABLE prompts ADD COLUMN current_version_id
UPDATE prompts SET current_version_id = (
  SELECT id FROM prompt_versions
  WHERE prompt_id = prompts.id AND version_number = 1
)

-- Step 4: Update foreign keys
ALTER TABLE prompts ADD FOREIGN KEY(current_version_id)
REFERENCES prompt_versions(id)

-- Step 5: Enable versioning on new updates
-- Application code now creates versions automatically
```

---

### 6.2 Diff Algorithm Implementation

**Use Python's difflib for unified diff:**

```python
import difflib
from typing import List

def generate_diff(content_v1: str, content_v2: str) -> str:
    """Generate unified diff between two versions."""
    lines_v1 = content_v1.splitlines(keepends=True)
    lines_v2 = content_v2.splitlines(keepends=True)

    diff = difflib.unified_diff(
        lines_v1,
        lines_v2,
        fromfile=f'Version 1',
        tofile=f'Version 2',
        lineterm=''
    )

    return ''.join(diff)

def generate_diff_with_stats(v1: str, v2: str) -> Dict[str, Any]:
    """Generate diff and statistics."""
    diff = generate_diff(v1, v2)

    lines_added = diff.count('\n+') - diff.count('\n+++')
    lines_removed = diff.count('\n-') - diff.count('\n---')

    # Similarity score using SequenceMatcher
    matcher = difflib.SequenceMatcher(None, v1, v2)
    similarity = matcher.ratio()

    return {
        "diff": diff,
        "lines_added": lines_added,
        "lines_removed": lines_removed,
        "similarity_score": round(similarity, 2)
    }
```

---

### 6.3 Pagination Best Practices

```python
def list_versions(
    prompt_id: str,
    page: int = 1,
    limit: int = 20
) -> VersionListResponse:
    """List versions with pagination."""

    # Validate
    assert page >= 1, "Page must be ≥1"
    assert 1 <= limit <= 100, "Limit must be 1-100"

    # Calculate offset
    offset = (page - 1) * limit

    # Query (with index on prompt_id, created_at)
    versions = db.query(PromptVersion) \
        .filter(PromptVersion.prompt_id == prompt_id) \
        .order_by(PromptVersion.created_at.desc()) \
        .offset(offset) \
        .limit(limit) \
        .all()

    # Total count (cached if available)
    total = db.query(func.count(PromptVersion.id)) \
        .filter(PromptVersion.prompt_id == prompt_id) \
        .scalar()

    # Response
    return VersionListResponse(
        versions=versions,
        total=total,
        page=page,
        limit=limit,
        pages=math.ceil(total / limit)
    )
```

---

## 7. Performance Considerations

### 7.1 Query Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| List versions (paginated) | <100ms | Index on (prompt_id, created_at) |
| Get single version | <50ms | Index on id |
| Compare versions | <500ms | May require full content loads |
| Restore version | <200ms | Includes version create + index update |
| Create version (on save) | <50ms | Overhead per prompt update |

### 7.2 Storage Efficiency

**Space Requirements (estimate: 1M prompts):**

```
Baseline (no versions):
  - Prompts: 1M × 1KB avg = 1GB

With versions (avg 5 versions per prompt):
  - Prompts: 1GB
  - Versions: 1M × 5 × 1KB = 5GB
  - Total: 6GB (6x baseline)

Optimizations:
  - Delta compression: Store diffs instead of full snapshots
  - Deduplication: Share identical content
  - Archival: Move old versions to cold storage
  - Cleanup: Retention policy (e.g., keep 1 year history)
```

### 7.3 Caching Strategy

```python
# Cache version list (1 hour TTL)
@cache.cached(timeout=3600, key_builder='version_list_{prompt_id}')
def get_versions_cached(prompt_id: str, page: int):
    return list_versions(prompt_id, page)

# Invalidate on restore
@on_restore
def invalidate_version_cache(prompt_id):
    cache.delete(f'version_list_{prompt_id}')

# Cache comparison (7 days TTL)
@cache.cached(timeout=604800, key_builder='version_compare_{v1}_{v2}')
def compare_versions_cached(v1_id, v2_id):
    return compare_versions(v1_id, v2_id)
```

---

## 8. Testing Strategy

### 8.1 Unit Tests

```python
# Tests for version creation
def test_create_version_on_prompt_create():
    """Creating a prompt creates version 1."""
    prompt = create_prompt(PromptCreate(...))
    assert prompt.version_count == 1
    versions = list_versions(prompt.id)
    assert len(versions) == 1
    assert versions[0].version_number == 1
    assert versions[0].is_current == True

def test_create_version_on_prompt_update():
    """Updating a prompt creates new version."""
    prompt = create_prompt(PromptCreate(...))
    assert prompt.version_count == 1

    updated = update_prompt(prompt.id, PromptUpdate(...))
    assert updated.version_count == 2

    versions = list_versions(prompt.id)
    assert len(versions) == 2

def test_restore_increments_version():
    """Restoring a version creates new version."""
    # Create → v1, Update → v2, Restore v1 → v3
    ...
```

### 8.2 Integration Tests

```python
def test_version_history_workflow():
    """End-to-end version workflow."""
    # Create
    prompt = client.post("/prompts", json={...}).json()
    assert prompt["version_count"] == 1

    # Update
    updated = client.put(f"/prompts/{prompt['id']}", json={...}).json()
    assert updated["version_count"] == 2

    # List versions
    versions = client.get(f"/prompts/{prompt['id']}/versions").json()
    assert versions["total"] == 2

    # Restore
    restored = client.post(
        f"/prompts/{prompt['id']}/versions/{versions[1]['id']}/restore",
        json={"summary": "test"}
    ).json()
    assert restored["version_count"] == 3
    assert restored["current_version_id"] != prompt["current_version_id"]
```

### 8.3 Edge Case Tests

```python
# Test rapid updates
# Test large content
# Test concurrent updates (future)
# Test version restoration with deleted collection
# Test comparison of identical versions
```

**Coverage Target**: 85%+ for versioning feature

---

## 9. Monitoring & Observability

### 9.1 Key Metrics to Track

```python
# Prometheus metrics
versions_created_total = Counter(
    'versions_created_total',
    'Total versions created',
    ['prompt_id']
)

versions_restored_total = Counter(
    'versions_restored_total',
    'Total versions restored'
)

comparison_duration_seconds = Histogram(
    'version_comparison_duration_seconds',
    'Time to compare two versions'
)

version_storage_bytes = Gauge(
    'version_storage_bytes',
    'Total bytes used by versions',
    ['prompt_id']
)
```

### 9.2 Logging

```python
# Log all version operations
logger.info(f"Version created: {version_id} (v{version_number}) for prompt {prompt_id}")
logger.info(f"Version restored: {version_id} → {new_version_id} for prompt {prompt_id}")
logger.warning(f"Failed to restore version: {version_id} (prompt deleted)")
```

---

## 10. Future Enhancements

### Phase 2 Features (Beyond Week 3)

- [ ] **Version Tags**: Label important versions (stable, production, etc.)
- [ ] **Branch/Merge**: Create version branches and merge strategies
- [ ] **Comments/Annotations**: Add notes to specific versions
- [ ] **Change Descriptions**: LLM-generated change summaries
- [ ] **Rollout Scheduling**: Schedule version activation
- [ ] **A/B Testing**: Compare prompt effectiveness across versions
- [ ] **Retention Policies**: Auto-delete old versions based on age/count
- [ ] **Audit Reports**: Generate compliance reports
- [ ] **Version Publishing**: Publish versions to prompt marketplace
- [ ] **Collaborative Reviews**: Multi-user version approval workflow

---

## 11. Success Criteria & Acceptance

### Definition of Done

- [x] Specification document complete and reviewed
- [ ] Data model designed and validated
- [ ] API endpoints specified with examples
- [ ] Edge cases documented
- [ ] Implementation started
- [ ] Unit tests written (85%+ coverage)
- [ ] Integration tests passing
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Tested with concurrent users
- [ ] Code reviewed and merged

### Sign-Off Checklist

- [ ] Product owner approves specification
- [ ] Tech lead approves architecture
- [ ] QA confirms test plan
- [ ] DevOps confirms deployment readiness

---

## 12. References & Related Documents

- [Project Brief](../PROJECT_BRIEF.md)
- [API Reference](../docs/API_REFERENCE.md)
- [Coding Standards](./.continuerules)
- [Database Schema Design Pattern](https://en.wikipedia.org/wiki/Audit_trail)
- [Unified Diff Format](https://tools.ietf.org/html/rfc3881)

---

**Document Status**: ✅ Ready for Implementation
**Last Updated**: February 27, 2026
**Next Review Date**: March 6, 2026 (Post-implementation)

---

## Appendix A: SQL Queries by Use Case

### Query 1: Get Latest 10 Versions

```sql
SELECT * FROM prompt_versions
WHERE prompt_id = ?
ORDER BY created_at DESC
LIMIT 10;

-- Index usage: idx_prompt_versions_created
```

### Query 2: Check if Prompt Has Versions

```sql
SELECT COUNT(*) as version_count
FROM prompt_versions
WHERE prompt_id = ?;
```

### Query 3: Get Current Version

```sql
SELECT * FROM prompt_versions
WHERE prompt_id = ?
AND is_current = TRUE;

-- Index usage: idx_prompt_versions_current
```

### Query 4: Restore a Version

```sql
BEGIN TRANSACTION;

-- Update old current version
UPDATE prompt_versions
SET is_current = FALSE
WHERE prompt_id = ? AND is_current = TRUE;

-- Create new version (application layer)
INSERT INTO prompt_versions (...) VALUES (...);

-- Update prompt's current_version_id
UPDATE prompts
SET current_version_id = ?,
    updated_at = NOW()
WHERE id = ?;

COMMIT;
```

---

## Appendix B: Example Implementation Flow (Pseudocode)

```python
# 1. CREATE PROMPT
def create_prompt(data: PromptCreate) -> Prompt:
    prompt = Prompt(id=uuid4(), **data.dict())
    storage.prompts[prompt.id] = prompt

    # Create version 1 automatically
    version = PromptVersion(
        id=uuid4(),
        prompt_id=prompt.id,
        version_number=1,
        title=prompt.title,
        content=prompt.content,
        # ... other fields
        is_current=True,
        created_at=datetime.utcnow()
    )
    storage.prompt_versions[version.id] = version
    prompt.current_version_id = version.id
    prompt.version_count = 1

    return prompt

# 2. UPDATE PROMPT
def update_prompt(prompt_id: str, data: PromptUpdate) -> Prompt:
    prompt = storage.prompts[prompt_id]

    # Update prompt
    for field, value in data.dict(exclude_unset=True).items():
        setattr(prompt, field, value)
    prompt.updated_at = datetime.utcnow()

    # Create new version
    old_version = storage.prompt_versions[prompt.current_version_id]
    old_version.is_current = False

    new_version = PromptVersion(
        id=uuid4(),
        prompt_id=prompt.id,
        version_number=prompt.version_count + 1,
        title=prompt.title,
        content=prompt.content,
        # ... copy all fields
        is_current=True,
        created_at=datetime.utcnow()
    )
    storage.prompt_versions[new_version.id] = new_version
    prompt.current_version_id = new_version.id
    prompt.version_count += 1

    return prompt

# 3. RESTORE VERSION
def restore_version(prompt_id: str, version_id: str, summary: str = None) -> Prompt:
    if not validate_restore(prompt_id, version_id):
        raise HTTPException(400, "Invalid restore")

    # Load version to restore
    version_to_restore = storage.prompt_versions[version_id]

    # Update prompt with version content
    prompt = storage.prompts[prompt_id]
    prompt.title = version_to_restore.title
    prompt.content = version_to_restore.content
    prompt.description = version_to_restore.description
    prompt.collection_id = version_to_restore.collection_id
    prompt.updated_at = datetime.utcnow()

    # Mark old current as not current
    old_version = storage.prompt_versions[prompt.current_version_id]
    old_version.is_current = False

    # Create restore version
    new_version = PromptVersion(
        id=uuid4(),
        prompt_id=prompt.id,
        version_number=prompt.version_count + 1,
        title=prompt.title,
        content=prompt.content,
        description=prompt.description,
        collection_id=prompt.collection_id,
        is_current=True,
        is_restored=True,
        change_summary=summary or f"Restored from version {version_to_restore.version_number}",
        created_at=datetime.utcnow()
    )
    storage.prompt_versions[new_version.id] = new_version
    prompt.current_version_id = new_version.id
    prompt.version_count += 1

    return prompt
```

---

## Appendix C: API Contract Examples (OpenAPI/Swagger)

```yaml
/prompts/{prompt_id}/versions:
  get:
    summary: List prompt versions
    parameters:
      - name: prompt_id
        in: path
        required: true
        schema: { type: string }
      - name: page
        in: query
        schema: { type: integer, default: 1 }
      - name: limit
        in: query
        schema: { type: integer, default: 20 }
    responses:
      200:
        description: Version list with pagination
        content:
          application/json:
            schema: { $ref: '#/components/schemas/VersionListResponse' }
      404:
        description: Prompt not found

/prompts/{prompt_id}/versions/{version_id}/compare/{version_id_2}:
  get:
    summary: Compare two versions
    parameters:
      - name: prompt_id
        in: path
        required: true
        schema: { type: string }
      - name: version_id
        in: path
        required: true
        schema: { type: string }
      - name: version_id_2
        in: path
        required: true
        schema: { type: string }
    responses:
      200:
        description: Version comparison with diff

/prompts/{prompt_id}/versions/{version_id}/restore:
  post:
    summary: Restore a version
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              summary:
                type: string
                maxLength: 500
    responses:
      201:
        description: Version restored successfully
        content:
          application/json:
            schema: { $ref: '#/components/schemas/Prompt' }
```
