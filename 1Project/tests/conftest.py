import os
import pytest
from persistence import AccessControlData, PICKLE_FILE_NAME

@pytest.fixture
def model():
    return AccessControlData.load_data()


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield

    if os.path.exists(PICKLE_FILE_NAME):
        os.remove(PICKLE_FILE_NAME)