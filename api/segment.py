import os
from PIL import Image
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
            
            # For segmentation, you can use simple image processing (Example: Convert to grayscale)
            segmented_img = img.convert('L')  # Convert to grayscale (simple segmentation)

            # Save the segmented image to a BytesIO object
            output = BytesIO()
            segmented_img.save(output, format='PNG')
            output.seek(0)
            
            # Return the segmented image as base64
            segmented_img_base64 = base64.b64encode(output.read()).decode('utf-8')
            
            return {
                "statusCode": 200,
                "body": json.dumps({"segmented_image": segmented_img_base64}),
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
