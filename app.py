from flask import Flask, render_template, request, make_response
import json
app = Flask(__name__)

main_page = "page2.html"

@app.route("/")
def index():
    return render_template(main_page)

if __name__ == "__main__":
    app.run()
