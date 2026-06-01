from flask import render_template

def register_routes(app):
    @app.route("/")
    def index():
        return render_template("chat.html")
    
    @app.route("/login")
    def login():
        return render_template("login.html")