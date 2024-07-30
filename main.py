from app import MyFrameApp

app = MyFrameApp()


# /home
@app.route('/home')
def home(request, response):
    response.text = "Hello from the Home Page"


# /about
@app.route("/about")
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
    response.body = app.template("home.html", context=context)