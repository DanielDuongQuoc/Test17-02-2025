from flask import Flask, render_template, request, redirect, url_for
from manage_sql import create_table
from controllers.property_controller import property_bp
import os
app = Flask(__name__)
# Cấu hình cho việc upload file
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'gif', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# Khởi tạo database
create_table()

@app.route('/')
def home():
    return render_template('base.html')

# Đăng ký blueprint cho các routes liên quan đến bất động sản
app.register_blueprint(property_bp)

if __name__ == '__main__':
    app.run(debug=True)