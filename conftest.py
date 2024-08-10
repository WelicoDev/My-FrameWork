import pytest
from myframeuz.app import MyFrameApp


@pytest.fixture
def app():
    return MyFrameApp()

@pytest.fixture
def test_client(app):
    return app.test_session()