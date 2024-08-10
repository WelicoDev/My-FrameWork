from myframeuz.app import MyFrameApp
from myframeuz.middleware import Middleware

app = MyFrameApp()


# /home
@app.route('/home', allowed_methods=["get"])
def home(request, response):
    response.text = "Hello from the Home Page"



# /about
@app.route("/about", allowed_methods=["put"])
def about(request, response):
    response.text = "Hello from the About Page"


@app.route('/hello/{name}')
def greeting(request, response, name):
    response.text = f"Hello {name}"

@app.route('/books')
class Book:
    def get(self, request, response):
        response.text = "Books Page"

    def post(self, request, response):
        response.text = "Endpoint to create a book"

def new_handler(request, response):
    response.text = "From new handler"


app.add_route('/new-handler', new_handler)

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
    # response.body = json.dumps(response_data).encode()
    # response.content_type = "application/json"

def on_exception(request, response, exc):
    response.text = str(exc)

app.add_exception_handler(on_exception)

@app.route('/exception')
def exception_trowing_handler(request, response):
    raise AttributeError("Some exception")

class LoggingMiddleware(Middleware):
    def __init__(self, app):
        super().__init__(app)
    def process_request(self, request):
        print("request is being called")

    def process_response(self, request, response):
        print("response has been generated")

app.add_middleware(LoggingMiddleware)