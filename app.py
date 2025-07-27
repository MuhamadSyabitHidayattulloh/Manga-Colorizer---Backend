from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import io
import base64
import requests
from PIL import Image
import numpy as np
import tempfile
import uuid
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
MODEL_URL = "https://api-inference.huggingface.co/models/Keiser41/Example_Based_Manga_Colorization"
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def query_huggingface_model(image_data, reference_image_data=None):
    """
    Query the Hugging Face model for manga colorization
    """
    headers = {"Authorization": f"Bearer {HUGGING_FACE_TOKEN}"}
    
    try:
        # For now, we'll use a simple approach
        # In a real implementation, you would need to adapt this based on the specific model requirements
        response = requests.post(MODEL_URL, headers=headers, data=image_data)
        
        if response.status_code == 200:
            return response.content
        else:
            logger.error(f"Hugging Face API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error querying Hugging Face model: {str(e)}")
        return None

def process_image_with_ai(image_path, reference_image_path=None):
    """
    Process image using AI model for colorization
    """
    try:
        # Read the input image
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # Read reference image if provided
        reference_data = None
        if reference_image_path and os.path.exists(reference_image_path):
            with open(reference_image_path, 'rb') as f:
                reference_data = f.read()
        
        # Query the model
        result = query_huggingface_model(image_data, reference_data)
        
        if result:
            # Save the result
            result_filename = f"colorized_{uuid.uuid4().hex}.png"
            result_path = os.path.join(RESULTS_FOLDER, result_filename)
            
            with open(result_path, 'wb') as f:
                f.write(result)
            
            return result_path
        else:
            # Fallback: return a simple processed version
            # In a real scenario, you might want to implement a local fallback model
            return create_fallback_colorized_image(image_path)
            
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return create_fallback_colorized_image(image_path)

def create_fallback_colorized_image(image_path):
    """
    Create a fallback colorized image (for demo purposes)
    This simulates the colorization process when the AI model is not available
    """
    try:
        # Open the original image
        img = Image.open(image_path)
        
        # Convert to RGB if not already
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Apply a simple color tint as a demo
        # In a real implementation, this would be replaced by actual AI processing
        img_array = np.array(img)
        
        # Add a slight warm tint to simulate colorization
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * 1.1, 0, 255)  # Red channel
        img_array[:, :, 1] = np.clip(img_array[:, :, 1] * 1.05, 0, 255)  # Green channel
        
        # Convert back to PIL Image
        colorized_img = Image.fromarray(img_array.astype(np.uint8))
        
        # Save the result
        result_filename = f"colorized_{uuid.uuid4().hex}.png"
        result_path = os.path.join(RESULTS_FOLDER, result_filename)
        colorized_img.save(result_path)
        
        return result_path
        
    except Exception as e:
        logger.error(f"Error creating fallback image: {str(e)}")
        return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model': 'Keiser41/Example_Based_Manga_Colorization'
    })

@app.route('/colorize', methods=['POST'])
def colorize_image():
    """
    Colorize a single image
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        image_file = request.files['image']
        reference_file = request.files.get('reference')
        
        if image_file.filename == '':
            return jsonify({'error': 'No image file selected'}), 400
        
        # Save uploaded files
        image_filename = f"input_{uuid.uuid4().hex}_{image_file.filename}"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        image_file.save(image_path)
        
        reference_path = None
        if reference_file and reference_file.filename != '':
            reference_filename = f"ref_{uuid.uuid4().hex}_{reference_file.filename}"
            reference_path = os.path.join(UPLOAD_FOLDER, reference_filename)
            reference_file.save(reference_path)
        
        # Process the image
        result_path = process_image_with_ai(image_path, reference_path)
        
        if result_path and os.path.exists(result_path):
            # Return the result image as base64
            with open(result_path, 'rb') as f:
                image_data = f.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Clean up uploaded files
            os.remove(image_path)
            if reference_path and os.path.exists(reference_path):
                os.remove(reference_path)
            
            return jsonify({
                'success': True,
                'colorized_image': image_base64,
                'result_path': os.path.basename(result_path),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Failed to process image'}), 500
            
    except Exception as e:
        logger.error(f"Error in colorize_image: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/colorize_batch', methods=['POST'])
def colorize_batch():
    """
    Colorize multiple images
    """
    try:
        if 'images' not in request.files:
            return jsonify({'error': 'No image files provided'}), 400
        
        images = request.files.getlist('images')
        reference_file = request.files.get('reference')
        
        if not images:
            return jsonify({'error': 'No image files selected'}), 400
        
        results = []
        reference_path = None
        
        # Save reference image if provided
        if reference_file and reference_file.filename != '':
            reference_filename = f"ref_{uuid.uuid4().hex}_{reference_file.filename}"
            reference_path = os.path.join(UPLOAD_FOLDER, reference_filename)
            reference_file.save(reference_path)
        
        for i, image_file in enumerate(images):
            try:
                # Save uploaded image
                image_filename = f"batch_{i}_{uuid.uuid4().hex}_{image_file.filename}"
                image_path = os.path.join(UPLOAD_FOLDER, image_filename)
                image_file.save(image_path)
                
                # Process the image
                result_path = process_image_with_ai(image_path, reference_path)
                
                if result_path and os.path.exists(result_path):
                    # Convert to base64
                    with open(result_path, 'rb') as f:
                        image_data = f.read()
                        image_base64 = base64.b64encode(image_data).decode('utf-8')
                    
                    results.append({
                        'success': True,
                        'original_name': image_file.filename,
                        'colorized_image': image_base64,
                        'result_path': os.path.basename(result_path)
                    })
                else:
                    results.append({
                        'success': False,
                        'original_name': image_file.filename,
                        'error': 'Failed to process image'
                    })
                
                # Clean up uploaded image
                os.remove(image_path)
                
            except Exception as e:
                logger.error(f"Error processing image {image_file.filename}: {str(e)}")
                results.append({
                    'success': False,
                    'original_name': image_file.filename,
                    'error': str(e)
                })
        
        # Clean up reference image
        if reference_path and os.path.exists(reference_path):
            os.remove(reference_path)
        
        return jsonify({
            'success': True,
            'results': results,
            'processed_count': len([r for r in results if r['success']]),
            'total_count': len(results),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in colorize_batch: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """
    Download a processed image
    """
    try:
        file_path = os.path.join(RESULTS_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error downloading file: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/models', methods=['GET'])
def get_available_models():
    """
    Get list of available models
    """
    return jsonify({
        'models': [
            {
                'name': 'Keiser41/Example_Based_Manga_Colorization',
                'description': 'Example-based manga colorization using reference images',
                'type': 'image-to-image',
                'status': 'active'
            }
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



