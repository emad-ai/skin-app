
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import keras.models
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf 

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the trained model
model = tf.keras.models.load_model('C:/Users/pc/Desktop/121/resnet101CNN.keras')

# Medical advice and treatment for each disease
MEDICAL_ADVICE = {
    'Chickenpox': {
        'message': 'The predicted disease is Chickenpox.',
        'advice': 'Ensure vaccination and avoid contact with infected individuals.',
        'treatment': 'Symptomatic relief with fever reducers and antihistamines; acyclovir for high-risk cases. Vaccination is essential for prevention.'
    },
    'Cowpox': {
        'message': 'The predicted disease is Cowpox.',
        'advice': 'Avoid direct contact with infected animals and wear gloves when handling cows.',
        'treatment': 'Usually self-limiting with supportive care. Antibiotics for secondary infections if needed.'
    },
    'HFMD': {
        'message': 'The predicted disease is Hand, Foot, and Mouth Disease (HFMD).',
        'advice': 'Maintain good hand hygiene and avoid sharing personal items.',
        'treatment': 'No specific treatment is required, but pain relievers and fever reducers can be used to ease symptoms.'
    },
    'Healthy': {
        'message': 'The skin appears healthy.',
        'advice': 'Continue maintaining a healthy lifestyle and personal hygiene.',
        'treatment': 'No treatment is needed.'
    },
    'Measles': {
        'message': 'The predicted disease is Measles.',
        'advice': 'Ensure vaccination against Measles and avoid direct contact with infected individuals.',
        'treatment': 'Treatment includes rest, plenty of fluids, and fever reducers. In some cases, Vitamin A may be recommended by a doctor.'
    },
    'Monkeypox': {
        'message': 'The predicted disease is Monkeypox.',
        'advice': 'Avoid direct contact with infected individuals or animals and wash your hands regularly.',
        'treatment': 'Supportive care and antiviral drugs like tecovirimat. Smallpox vaccine can provide protection.'
    }
}

# Predict the disease from the image
def get_prediction(img, model, labels=[
    'Chickenpox', 'Cowpox', 'HFMD', 'Healthy', 'Measles', 'Monkeypox'
], target_size=(224, 224)):
    class_names = labels
    img = tf.keras.utils.load_img(img, target_size=target_size)
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    prediction = model.predict(img_array)
    score = [tf.nn.softmax(prediction)[0][i].numpy() * 100 for i in range(len(class_names))]
    result = sorted([(class_names[i], f"{score[i]:.2f}%") for i in range(len(class_names))], key=lambda x: float(x[1].replace('%', '')), reverse=True)
    highest_label = result[0][0]  # The most likely class
    return result, highest_label

# Save the image to the appropriate folder
def save_image_to_class_folder(file_path, label):
    class_folder = os.path.join(app.config['UPLOAD_FOLDER'], label)
    if not os.path.exists(class_folder):
        os.makedirs(class_folder)  # Create the folder if it doesn't exist
    new_file_path = os.path.join(class_folder, os.path.basename(file_path))
    os.rename(file_path, new_file_path)  # Move the image to the appropriate folder
    return new_file_path

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Diagnosis page
@app.route('/diagnose', methods=['GET', 'POST'])
def diagnose():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Get prediction and highest class
            result, highest_label = get_prediction(file_path, model)

            # Save the image to the appropriate folder
            saved_file_path = save_image_to_class_folder(file_path, highest_label)

            # Fetch medical advice and treatment
            message = MEDICAL_ADVICE[highest_label]['message']
            advice = MEDICAL_ADVICE[highest_label]['advice']
            treatment = MEDICAL_ADVICE[highest_label]['treatment']

            return render_template(
                'diagnose.html',
                diagnosis=result,
                image_url=saved_file_path,
                message=message,
                advice=advice,
                treatment=treatment
            )
    return render_template('diagnose.html', diagnosis=None)

if __name__ == '__main__':
  
  app.run(host='0.0.0.0', port=5000, debug=True)

