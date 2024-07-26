from app import MyFrameApp

app = MyFrameApp()

# /home
@app.route('/home')
def home(request , response):
    response.text = "Hello from the Home Page"

# /about
@app.route("/about")
def about(request , response):
    response.text = "Hello from the About Page"

@app.route('/hello/{name}')
def greeting(request, response, name):
    response.text = f"Hello {name}"