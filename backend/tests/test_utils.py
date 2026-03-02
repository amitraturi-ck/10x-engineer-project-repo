from datetime import datetime, timedelta
from app.models import Prompt
from app.utils import sort_prompts_by_date
from app.utils import filter_prompts_by_collection
from app.utils import search_prompts
from app.utils import validate_prompt_content
from app.utils import extract_variables

def make_prompt(title: str, dt: datetime):
    return Prompt(
        id=title,
        title=title,
        content="Some valid prompt content",
        description=None,
        collection_id=None,
        created_at=dt,
        updated_at=dt,
    )


def test_sort_prompts_descending():
    now = datetime.utcnow()
    older = now - timedelta(days=1)

    p1 = make_prompt("old", older)
    p2 = make_prompt("new", now)

    sorted_list = sort_prompts_by_date([p1, p2])

    assert sorted_list[0].title == "new"
    assert sorted_list[1].title == "old"


def test_sort_prompts_ascending():
    now = datetime.utcnow()
    older = now - timedelta(days=1)

    p1 = make_prompt("old", older)
    p2 = make_prompt("new", now)

    sorted_list = sort_prompts_by_date([p1, p2], descending=False)

    assert sorted_list[0].title == "old"


def test_filter_prompts_by_collection_match():
    p1 = make_prompt("a", datetime.utcnow())
    p1.collection_id = "col1"

    p2 = make_prompt("b", datetime.utcnow())
    p2.collection_id = "col2"

    result = filter_prompts_by_collection([p1, p2], "col1")

    assert len(result) == 1
    assert result[0].title == "a"


def test_filter_prompts_by_collection_empty():
    p1 = make_prompt("a", datetime.utcnow())
    p1.collection_id = "colX"

    result = filter_prompts_by_collection([p1], "missing")

    assert result == []


def test_search_by_title_case_insensitive():
    p = make_prompt("Email Writer", datetime.utcnow())
    p.description = None

    result = search_prompts([p], "email")

    assert len(result) == 1


def test_search_by_description():
    p = make_prompt("Other", datetime.utcnow())
    p.description = "Generate a sales email"

    result = search_prompts([p], "sales")

    assert len(result) == 1


def test_search_no_results():
    p = make_prompt("Hello", datetime.utcnow())
    p.description = None

    result = search_prompts([p], "missing")

    assert result == []


def test_validate_empty():
    assert validate_prompt_content("") is False


def test_validate_whitespace():
    assert validate_prompt_content("   ") is False


def test_validate_too_short():
    assert validate_prompt_content(" short ") is False


def test_validate_valid():
    assert validate_prompt_content("This is a valid prompt.") is True


def test_extract_multiple_variables():
    text = "Hello {{first}} {{last}}"
    result = extract_variables(text)

    assert result == ["first", "last"]


def test_extract_no_variables():
    assert extract_variables("Hello world") == []


def test_extract_ignores_invalid():
    text = "Hello {{valid}} {{not-valid}}"
    result = extract_variables(text)

    assert result == ["valid"]
