import os
from PIL import Image, ImageEnhance
import json
from io import BytesIO
import base64

def handler(request):
    if request.method == "POST":
        try:
            # Get image from request (assumed as base64-encoded string)
            data = json.loads(request.body.decode())
            img_data = base64.b64decode(data['image'])
            
            # Open image
            img = Image.open(BytesIO(img_data))
            
            # Enhance image (Example: Increase brightness)
            enhancer = ImageEnhance.Brightness(img)
            enhanced_img = enhancer.enhance(1.5)  # Adjust this factor as needed
            
            # Save the enhanced image to a BytesIO object
            output = BytesIO()
            enhanced_img.save(output, format='PNG')
            output.seek(0)
            
            # Return the enhanced image as base64
            enhanced_img_base64 = base64.b64encode(output.read()).decode('utf-8')
            
            return {
                "statusCode": 200,
                "body": json.dumps({"enhanced_image": enhanced_img_base64}),
                "headers": {
                    "Content-Type": "application/json"
                }
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)}),
                "headers": {
                    "Content-Type": "application/json"
                }
            }

    return {
        "statusCode": 405,
        "body": json.dumps({"error": "Method not allowed"}),
        "headers": {
            "Content-Type": "application/json"
        }
    }
