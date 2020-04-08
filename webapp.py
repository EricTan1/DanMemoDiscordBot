from flask import Flask, render_template, url_for, request
 
webapp = Flask(__name__)

@webapp.route('/')
@webapp.route('/index/')
def index():
    return "Hello world!"

'''@webapp.route('/calculator/')
def calculator():
    return render_template("calculator.html",
        bootstrap_css=url_for("static", filename="css/bootstrap/bootstrap.css"),    #//netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css
        bootstrap_js=url_for("static", filename="js/bootstrap/bootstrap.js"),       #//netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js
        jquery_js=url_for("static", filename="js/jquery/jquery.js"),                #//code.jquery.com/jquery-1.11.1.min.js
        url_css=url_for("static", filename="css/calculator.css"),
        css_autocomplete=url_for("static", filename="css/autocomplete.css"),
        js_autocomplete=url_for("static", filename="js/autocomplete.js"),
        html_autocomplete=url_for("static", filename="list.html"),
        url_js=url_for("static", filename="js/calculator.js"))'''

if __name__ == "__main__":
    webapp.run()