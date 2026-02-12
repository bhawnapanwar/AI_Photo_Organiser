import os
import json
import shutil
import io
import time
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image, ImageOps 

def analyze_and_organize_photos(source_dir, dest_dir):
    load_dotenv()
    endpoint = os.getenv("AZURE_ENDPOINT")
    key = os.getenv("AZURE_KEY")

    SOURCE_FOLDER = source_dir
    DESTINATION_FOLDER = dest_dir
    
    client = ComputerVisionClient(
        endpoint=endpoint,
        credentials=CognitiveServicesCredentials(key)
    )

    os.makedirs(DESTINATION_FOLDER, exist_ok=True)
    all_metadata = [] 

    print(f"Starting photo organization...")
    

    for filename in os.listdir(SOURCE_FOLDER):
        image_path = os.path.join(SOURCE_FOLDER, filename)
        
        # Check extensions
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            continue

        print(f"--- Processing: {filename} ---")

        try:
            
            
            image_stream = io.BytesIO()

            with Image.open(image_path) as img:
                
                
                img = ImageOps.exif_transpose(img)

                # 2. Convert to RGB 
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                
                max_size = (1200, 1200)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                
                img.save(image_stream, format="JPEG", quality=70)
                

                # 6. Reset stream pointer to the beginning!
                image_stream.seek(0)

            

           
            features = [
                VisualFeatureTypes.objects,
                VisualFeatureTypes.tags,
                VisualFeatureTypes.description,
                VisualFeatureTypes.color 
            ]
            
            
            result = client.analyze_image_in_stream(
                image_stream,
                visual_features=features,
                language="en"
            )

            # 5. Extract Data
            detected_items = set()
            
            # Tags
            photo_tags = []
            if result.tags:
                for tag in result.tags:
                    if tag.confidence > 0.6:
                        detected_items.add(tag.name)
                        photo_tags.append(tag.name)
            
            # Objects
            photo_objects = []
            if result.objects:
                for obj in result.objects:
                    obj_name = obj.object_property 
                    detected_items.add(obj_name)
                    photo_objects.append(obj_name)

            # Description & Confidence
            photo_description = "No description available."
            caption_confidence = 0.0
            if result.description and result.description.captions:
                caption_obj = result.description.captions[0]
                photo_description = caption_obj.text
                caption_confidence = caption_obj.confidence 

            # Colors
            dominant_colors = []
            accent_color = ""
            if result.color:
                dominant_colors = result.color.dominant_colors
                accent_color = result.color.accent_color

            # 6. Store Metadata
            photo_metadata = {
                "file": filename,
                "description": photo_description,
                "confidence_score": caption_confidence,
                "dominant_colors": dominant_colors,
                "accent_color": accent_color,
                "objects_detected": photo_objects,
                "tags": photo_tags
            }
            all_metadata.append(photo_metadata)
            
            # 7. Copy file
            if not detected_items:
                print(f"  > No confident items detected.")
            else:
                print(f"  > Found: {', '.join(detected_items)}")
                for item in detected_items:
                    folder_name = item.replace(" ", "_").lower()
                    target_folder = os.path.join(DESTINATION_FOLDER, folder_name)
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.copy(image_path, os.path.join(target_folder, filename))
                print(f"  > Copied to {len(detected_items)} folder(s).")

            
            time.sleep(1)

        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # 8. Write metadata.json
    metadata_file_path = os.path.join(DESTINATION_FOLDER, "metadata.json")
    with open(metadata_file_path, 'w') as f:
        json.dump(all_metadata, f, indent=4)

    print(f"\nProcessing complete!")
    print(f"Metadata file saved to: {metadata_file_path}")

if __name__ == "__main__":
    SOURCE_DIR = "source_photos"
    DEST_DIR = "organized_photos"
    analyze_and_organize_photos(SOURCE_DIR, DEST_DIR)