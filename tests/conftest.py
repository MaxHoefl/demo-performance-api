import pytest

from app.data_acess.models import Base


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base