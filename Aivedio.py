from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
from PIL import Image
import requests
import io
import cloudinary
import cloudinary.uploader

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Hugging Face API Configuration
HF_API_TOKEN = "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"  # Replace with your HF API token
HF_MODEL_ID = "prithivMLmods/Flux-Product-Ad-Backdrop"   # Hugging Face Model ID
client = InferenceClient(HF_MODEL_ID, token=HF_API_TOKEN)

# RunwayML API Configuration
RUNWAYML_URL = "https://runwayml.p.rapidapi.com/generate/imageDescription"
RUNWAYML_HEADERS = {
    "x-rapidapi-key": "c4149d7f42msh169b1ac1d7c079ep17cebfjsn882b5a92dacd",  # Replace with RunwayML key
    "x-rapidapi-host": "runwayml.p.rapidapi.com",
    "Content-Type": "application/json"
}

# Cloudinary Configuration
cloudinary.config(
    cloud_name="dkr5qwdjd",  # Replace with your Cloudinary Cloud Name
    api_key="797349366477678",  # Replace with your Cloudinary API Key
    api_secret="9HUrfG_i566NzrCZUVxKyCHTG9U"  # Replace with your Cloudinary API Secret
)

@app.route('/generate_video', methods=['GET', 'POST'])
def generate_video():
    try:
        if request.method == 'GET':
            prompt = request.args.get("prompt")
        elif request.method == 'POST':
            data = request.get_json()
            prompt = data.get('prompt') if data else None

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        print(f"Received prompt: {prompt}")
        
        # Remaining code here...

    

        # Step 1: Generate Image from Hugging Face API
        try:
            print("Generating image using Hugging Face API...")
            image = client.text_to_image(prompt)

            if not isinstance(image, Image.Image):
                return jsonify({"error": "Failed to generate an image"}), 500

            # Save the image temporarily in memory
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes.seek(0)
            print("Image generated successfully!")
        except Exception as e:
            print(f"Error generating image: {str(e)}")
            return jsonify({"error": f"Error generating image: {str(e)}"}), 500

        # Step 2: Upload Image to Cloudinary
        try:
            print("Uploading image to Cloudinary...")
            upload_result = cloudinary.uploader.upload(image_bytes, folder="generated_images")
            cloudinary_url = upload_result.get("secure_url")
            if not cloudinary_url:
                raise ValueError("Failed to retrieve Cloudinary URL.")
            print(f"Image uploaded successfully to Cloudinary: {cloudinary_url}")
        except Exception as e:
            print(f"Error uploading image to Cloudinary: {str(e)}")
            return jsonify({"error": f"Error uploading image to Cloudinary: {str(e)}"}), 500

        # Step 3: Generate Video using RunwayML
       

        # Step 4: Return Response
        return jsonify({
            "message": "Video generated successfully!",
            "image_url": cloudinary_url,
            
        }), 200

    except Exception as e:
        print(f"Internal server error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


# Run Flask Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
