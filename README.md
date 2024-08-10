# MyFrameWork: Python Web Framework built for learning purposes

![purpose](https://img.shields.io/badge/purpose-learning-green)
![PyPI - Version](https://img.shields.io/pypi/v/myframeuz)

MyFrameUz is a Python web framework built for learning purposes.

It's a WSGI framework and can be used with any WSGI application server such as Gunicorn.

## Installation

```shell
pip install myframeuz
```

## How to use it

### Basic usage:


```python
from myframeuz.app import MyFrameApp

app = MyFrameApp()

@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"

@app.route("hello/{name}/")
def greeting(request, response, name):
    response.text = f"Hello, {name}"

@app.route('/books')
class Book:
    def get(self, request, response):
        response.text = "Books Page"

    def post(self, request, response):
        response.text = "Endpoint to create a book"

@app.route('/template')
def template_handler(request, response):
    context = {
        "title":"New Project",
        "content":"New FastApi Project"
               }
    response.html = app.template("home.html", context=context)

@app.route("/json")
def json_handler(request, response):
    response_data = {"name": "same name", "type":"json"}
    response.json = response_data
```

### Unit Tests

The recommended way of writing unit tests is with [pytest](https://docs.pytest.org/en/latest/). There are teo
built in fixtures that you may want to use when writing unit tests with MyFrameUz. The first one is 'app' which is
an instance of the main 'MyFrameUz' class:

```python
import pytest
from conftest import app
from myframeuz.middleware import Middleware

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
```

## Templates

The default folder for templates is 'templates'. You can change it when initializing the main MyFrameApp() class :

```python
app = MyFrameApp(templates="templates_dir_name")
```

The you can use HTML files in that folder like so in a handler:

```python
@app.route('show/template')
def template_handler(request, response):
    context = {
        "title":"New Project",
        "content":"New FastApi Project"
               }
    response.html = app.template("home.html", context=context)
```

## Static Files 

Just like templates, the default folder for static files is 'static' nd you can override it:

```python
app = MyFrameApp(static_dir = "static_dir_name")
```

The you can use the files inside this folder in HTML files:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Assalom aleykum</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>Welcome to my framework</h1>
    <p>{{title}}</p>
    <p>{{content}}</p>
</body>
</html>
```

### Middleware 

    You can create custom middleware classes by inhereting from the "myframeuz.middleware.Middleware"
    class and overriding its two methods that are called before and after each request:

```python
from myframeuz.app import MyFrameApp
from myframeuz.middleware import Middleware

from webob import Request


class Middleware:
    def __init__(self, app):
        self.app = app

    def add(self, middleware_class):
        self.app = middleware_class(self.app)

    def process_request(self, request):
        pass

    def process_response(self, request, response):
        pass

    def handle_request(self, request):
        self.process_request(request)
        response = self.app.handle_request(request)
        self.process_response(request, response)

        return response

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.app.handle_request(request)
        return response(environ, start_response)
```