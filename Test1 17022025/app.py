from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from manage_sql import add_property, update_property, delete_property, list_properties, search_properties

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/properties", methods=["GET", "POST"])
def properties():
    if request.method == "POST":
        data = request.form
        add_property(data["property_name"], data["location"], data["type"], data["price"], data["status"])
        return redirect(url_for("properties"))
    properties = list_properties()
    return render_template("properties.html", properties=properties)

@app.route("/manage", methods=["GET", "POST"])
def manage():
    if request.method == "POST":
        data = request.form
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            image_url = None
        add_property(data["property_name"], data["location"], data["type"], data["price"], data["status"], image_url)
        return redirect(url_for("manage"))
    properties = list_properties()
    return render_template("manage.html", properties=properties)

@app.route("/properties/search", methods=["GET"])
def search():
    keyword = request.args.get("keyword", "")
    results = search_properties(keyword)
    return render_template("properties.html", properties=results)

@app.route("/properties/<int:property_id>/edit", methods=["GET", "POST"])
def edit_property(property_id):
    if request.method == "POST":
        data = request.form
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            image_url = None
        update_property(property_id, data["property_name"], data["location"], data["type"], data["price"], data["status"], image_url)
        return redirect(url_for("manage"))
    properties = list_properties()
    property_to_edit = next((prop for prop in properties if prop[0] == property_id), None)
    return render_template("edit_property.html", property=property_to_edit)

@app.route("/properties/<int:property_id>/delete", methods=["POST"])
def remove_property(property_id):
    delete_property(property_id)
    return redirect(url_for("manage"))

if __name__ == "__main__":
    app.run(debug=True)