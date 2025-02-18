import os
from flask import Blueprint, render_template, request, redirect, url_for, Flask
from models.property_model import get_properties, add_property, update_property, delete_property, search_properties
from werkzeug.utils import secure_filename

property_bp = Blueprint('property', __name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    unique_id = hex(int.from_bytes(os.urandom(4), byteorder='big'))[2:]
    return f"{base}_{unique_id}{ext}"

@property_bp.route('/products')
def show_properties():
    properties = get_properties()
    return render_template('list.html', properties=properties)

@property_bp.route('/manage')
def manage_properties():
    properties = get_properties()
    return render_template('manage.html', properties=properties)

@property_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        property_name = request.form['property_name']
        location = request.form['location']
        property_type = request.form['type']
        price = float(request.form['price'])
        status = request.form['status']
        description = request.form.get('description')
        specs = request.form.get('specs')
        area = request.form.get('area')
        bathrooms = request.form.get('bathrooms')
        bedrooms = request.form.get('bedrooms')
        direction = request.form.get('direction')

        image_url_db = None  # Initialize image_url_db to None

        if 'image_upload' in request.files:
            file = request.files['image_upload']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = generate_unique_filename(filename)
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(file_path)
                image_url_db = url_for('static', filename='uploads/' + unique_filename)
            elif request.form.get('image_url'): # If upload failed or no file uploaded but URL is provided
                image_url_db = request.form.get('image_url')
        elif request.form.get('image_url'): # If no file upload attempt, but URL is provided
            image_url_db = request.form.get('image_url')

        add_property(property_name, location, property_type, price, status, image_url_db, description, specs, area, bathrooms, bedrooms, direction)
        return redirect(url_for('property.manage_properties'))
    return render_template('add_property.html')

@property_bp.route('/update/<int:property_id>', methods=['POST'])
def update(property_id):
    property_name = request.form['property_name']
    location = request.form['location']
    property_type = request.form['type']
    price = float(request.form['price'])
    status = request.form['status']
    update_property(property_id, property_name, location, property_type, price, status)
    return redirect(url_for('home')) # Change to property.manage_properties if you want to redirect to manage page

@property_bp.route('/search', methods=['GET'])
def search():
    search_type = request.args.get('search_type')
    property_type = request.args.get('property_type')
    location = request.args.get('location')
    street = request.args.get('street')
    price_range = request.args.get('price_range')
    area = request.args.get('area')
    bathrooms = request.args.get('bathrooms')
    bedrooms = request.args.get('bedrooms')
    direction = request.args.get('direction')

    results = search_properties(search_type, property_type, location, street, price_range, area, bathrooms, bedrooms, direction)
    return render_template('search_results.html', properties=results)

@property_bp.route('/delete/<int:property_id>', methods=['POST'])
def delete(property_id):
    delete_property(property_id)
    return redirect(url_for('property.manage_properties')) # Change to property.manage_properties if you want to redirect to manage page