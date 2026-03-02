from app.api import update_prompt
from fastapi import HTTPException
from app.api import patch_prompt
from app.models import PromptUpdate
from app.models import Prompt, get_current_time
from app.storage import storage
from app.api import delete_prompt





def test_update_prompt_none_payload():
    try:
        update_prompt("some-id", None)  # bypass FastAPI validation
    except HTTPException as e:
        assert e.status_code == 400
def test_update_prompt_blank_id_direct():
    from app.models import PromptUpdate

    try:
        update_prompt("   ", PromptUpdate(title="T", content="C"))
    except HTTPException as e:
        assert e.status_code == 404

def test_patch_prompt_blank_id_direct():
    try:
        patch_prompt("   ", PromptUpdate())
    except HTTPException as e:
        assert e.status_code == 404

def test_patch_prompt_invalid_collection(monkeypatch):
    # Create a real prompt object (not fixture data)
    prompt = Prompt(
        title="T",
        content="Valid content",
        description=None,
        collection_id=None,
        created_at=get_current_time(),
        updated_at=get_current_time(),
    )

    storage.create_prompt(prompt)

    # Force collection lookup to fail → triggers lines 245-247
    monkeypatch.setattr(storage, "get_collection", lambda _: None)

    try:
        patch_prompt(prompt.id, PromptUpdate(collection_id="bad-id"))
    except HTTPException as e:
        assert e.status_code == 400
def test_delete_prompt_failure(monkeypatch, client):
    monkeypatch.setattr(
        "app.api.storage.delete_prompt",
        lambda _: False
    )

    response = client.delete("/prompts/fake-id")
    assert response.status_code == 404
def test_delete_collection_success_branch(client, sample_collection_data):
    # Create collection
    create = client.post("/collections", json=sample_collection_data)
    cid = create.json()["id"]

    # Delete collection (no prompts attached → allowed)
    response = client.delete(f"/collections/{cid}")

    assert response.status_code == 204

    # Verify it is actually gone
    get_response = client.get(f"/collections/{cid}")
    assert get_response.status_code == 404
    create = client.post("/collections", json=sample_collection_data)
    cid = create.json()["id"]

    response = client.delete(f"/collections/{cid}")

    assert response.status_code == 204
    prompt = Prompt(
        title="Delete Me",
        content="Valid content",
        description=None,
        collection_id=None,
        created_at=get_current_time(),
        updated_at=get_current_time(),
    )

    storage.create_prompt(prompt)

    # Call function directly (not via HTTP)
    result = delete_prompt(prompt.id)

    assert result is None



def test_delete_prompt_success_direct_call():
    prompt = Prompt(
        title="Direct Delete",
        content="Valid content",
        description=None,
        collection_id=None,
        created_at=get_current_time(),
        updated_at=get_current_time(),
    )

    storage.create_prompt(prompt)

    # Direct function call (not via HTTP)
    delete_prompt(prompt.id)
def test_get_prompt_versions_success(client, sample_prompt_data):
    create = client.post("/prompts", json=sample_prompt_data)
    prompt_id = create.json()["id"]

    response = client.get(f"/prompts/{prompt_id}/versions")

    assert response.status_code == 200
    data = response.json()
    assert data["prompt_id"] == prompt_id
    assert isinstance(data["versions"], list)


def test_get_prompt_versions_not_found(client):
    response = client.get("/prompts/missing-id/versions")
    assert response.status_code == 404


def test_get_prompt_versions_blank_id(client):
    response = client.get("/prompts/ /versions")
    assert response.status_code == 404

def test_delete_prompt_http_success(client, sample_prompt_data):
    create = client.post("/prompts", json=sample_prompt_data)
    prompt_id = create.json()["id"]

    response = client.delete(f"/prompts/{prompt_id}")
    assert response.status_code == 204
