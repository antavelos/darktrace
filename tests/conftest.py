import pytest
from pkg_resources import resource_filename
from tinydb import TinyDB


@pytest.fixture(scope="module", autouse=True)
def test_db():
    db_file = resource_filename(__name__, "test_db.json")

    # empty db file
    with open(db_file, "w"):
        pass

    db = TinyDB(db_file)

    return db
