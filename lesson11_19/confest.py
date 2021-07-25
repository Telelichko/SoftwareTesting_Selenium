import pytest
from python_tests.lesson11_19.App.Application import Application


@pytest.fixture
def app(request):
    app = Application()
    app.driver.implicitly_wait(3)
    request.addfinalizer(app.driver.quit)
    return app