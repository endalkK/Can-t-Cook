from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import io

from recipe_class import Recipes

app = Flask(__name__)

recipe = Recipes()

# Load TFLite model and allocate tensors
interpreter = tf.lite.Interpreter(model_path="model_unquant.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

labels = ['carrot','broccoli', 'brown rice', 'chicken Breast', 'chicken thigh', 'chicken wings','egg','lemon', 'corn','peprika', 'pork belly', 'potato', 'strawberry', 'tofu' 'salmon' 'white rice', 'tomato']  # Modify based on your labels

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    image =  Image.open(io.BytesIO(image_file.read())).convert("RGB")
    image = image.resize((input_details[0]['shape'][1], input_details[0]['shape'][2]))

    image_array = np.asarray(image, dtype=np.float32) / 255.0
    image_data = np.expand_dims(image_array, axis=0)

    # Make prediction
    interpreter.set_tensor(input_details[0]['index'], image_data)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])
    predicted_index = np.argmax(predictions[0])
    
    response = {
        'prediction': labels[predicted_index],
        'confidence': float(predictions[0][predicted_index])
    }
    return jsonify(response)

@app.route('/recipe', methods=['POST'])
def generate_recipe():
    try: 
        data = request.get_json()
        scanned_items = data.get('ingredients', [])
        print(scanned_items)
        return jsonify(recipe.generate_instructions(scanned_items)), 200
    except:
        return jsonify({'error': 'No ingredients provided'}), 400

if __name__ == '__main__':
    app.run(debug=False)
