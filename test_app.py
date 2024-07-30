import pytest
from conftest import app

def test_basic_route_adding(app):
    @app.route('/home')
    def home(request, response):
        response.text = "Hello from Home"

def test_duplicate_routes_throws_exception(app):
    @app.route('/home')
    def home(request, response):
        response.text = "Hello from Home"

    with pytest.raises(AssertionError):
        @app.route('/home')
        def home(request, response):
            response.text = "Hello from Home 2"

def test_requests_can_be_sent_by_test_client(app, test_client):
    @app.route('/home')
    def home(request, response):
        response.text = "Hello from home"

    response = test_client.get("http://testserver/home")
    assert response.text == "Hello from home"

def test_parameterized_routing(app, test_client):
    @app.route('/hello/{name}')
    def greeting(request, response, name):
        response.text = f"Hello {name}"
    assert test_client.get("http://testserver/hello/Tom").text == "Hello Tom"
    assert test_client.get("http://testserver/hello/Alisa").text == "Hello Alisa"

def test_default_response(app, test_client):
    response = test_client.get("http://testserver/noneexistent")

    assert response.text == "Not Found 404"
    assert response.status_code == 404

def test_class_based_get(app, test_client):
    @app.route('/books')
    class Book:
        def get(self, request, response):
            response.text = "Books Page"

    assert test_client.get("http://testserver/books").text == "Books Page"

def test_class_based_post(app, test_client):
    @app.route('/books')
    class Book:
        def post(self, request, response):
            response.text = "Endpoint to create a book"

    assert test_client.post("http://testserver/books").text == "Endpoint to create a book"

def test_class_based_method_not_allowed(app, test_client):
    @app.route('/books')
    class Book:
        def post(self, request, response):
            response.text = "Endpoint to create a book"

    response = test_client.get('http://testserver/books')

    assert response.text == "Method Not Allowed"
    assert response.status_code == 405

def test_alternative_route_adding(app, test_client):
    def new_handler(request, response):
        response.text = "From new handler"

    app.add_route('/new-handler', new_handler)

    assert test_client.get("http://testserver/new-handler").text == "From new handler"

def test_template_handler(app, test_client):
    @app.route("/test-template")
    def template(request, response):
        context = {"title":"New Project",
                   "content":"FastApi project"
                   }
        response.body = app.template("test.html", context=context)

    response = test_client.get("http://testserver/test-template")

    assert "New Project" in response.text
    assert "FastApi project" in response.text
    assert "text/html" in response.headers["Content-Type"]

def test_custom_exception_handler(app, test_client):
    def on_exception(request, response, exc):
        response.text = "Something bad happened"

    app.add_exception_handler(on_exception)

    @app.route('/exception')
    def exception_trowing_handler(request, response):
        raise AttributeError("Some exception")

    response = test_client.get("http://testserver/exception")

    assert response.text == "Something bad happened"

def test_none_existent_static_file(test_client):
    assert test_client.get("http://testserver/nonexitent.css").status_code == 404

def test_serving_static_file(test_client):
    response = test_client.get("http://testserver/test.css")

    assert response.text == "body {background-color: green;}"