from app.storage import Storage
from app.models import Prompt, get_current_time


def test_update_prompt_missing_id_returns_none():
    storage = Storage()

    prompt = Prompt(
        title="T",
        content="Valid content",
        created_at=get_current_time(),
        updated_at=get_current_time(),
    )

    result = storage.update_prompt("does-not-exist", prompt)

    assert result is None  # covers line 96


def test_delete_collection_missing_returns_false():
    storage = Storage()

    result = storage.delete_collection("missing-id")

    assert result is False  # covers line 182


def test_get_prompts_by_collection_empty():
    storage = Storage()

    prompts = storage.get_prompts_by_collection("no-match")

    assert prompts == []  # covers line 197
