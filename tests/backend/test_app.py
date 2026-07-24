import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


@pytest.fixture
def client():
    return TestClient(app_module.app)


def test_unregister_participant_removes_email_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": participant_email},
    )

    # Assert
    assert response.status_code == 200
    assert participant_email not in app_module.activities[activity_name]["participants"]


def test_unregister_returns_error_for_participant_not_registered(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": participant_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
