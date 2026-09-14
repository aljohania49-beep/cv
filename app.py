```python
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)

# إعداد مجلد حفظ الصور المرفوعة
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cm')
def cm():
    return render_template('cm.html')

@app.route('/generate_cv', methods=['POST'])
def generate_cv():
    full_name = request.form.get('full_name')
    job_title = request.form.get('job_title')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address', 'المملكة العربية السعودية')
    summary = request.form.get('summary')
    experience = request.form.get('experience')
    education = request.form.get('education')
    skills = request.form.get('skills')
    languages = request.form.get('languages', 'اللغة العربية (اللغة الأم)، اللغة الإنجليزية (متقدم)')
    
    # معالجة رفع الصورة الشخصية
    photo_filename = None
    if 'photo' in request.files:
        file = request.files['photo']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # إضافة بادئة زمنية لاسم الملف لمنع التكرار
            photo_filename = f"{int(time.time())}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
            
    return render_template('cv_template.html', 
                           full_name=full_name, 
                           job_title=job_title, 
                           email=email, 
                           phone=phone, 
                           address=address,
                           summary=summary, 
                           experience=experience, 
                           education=education, 
                           skills=skills,
                           languages=languages,
                           photo=photo_filename)

# إتاحة ملف robots.txt لمحركات البحث
@app.route('/robots.txt')
def robots():
    return send_from_directory('.', 'robots.txt')

# إتاحة ملف sitemap.xml لمحركات البحث
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```
