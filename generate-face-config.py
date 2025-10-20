#!/usr/bin/env python3
"""
Generate faces-config.json by reading image dimensions and detecting
alignment points using bottom-most dark pixels.
"""

import json
import os
import numpy as np
from PIL import Image

def get_image_dimensions(image_path):
    """Get width and height of an image."""
    with Image.open(image_path) as img:
        return img.size  # returns (width, height)

def find_bottom_dark_pixels(image_path, darkness_threshold=100):
    """
    Find the bottom-left and bottom-right dark pixels for alignment.
    Returns (left_x, left_y, right_x, right_y, body_bottom_y)
    """
    with Image.open(image_path) as img:
        # Convert to numpy array for easier processing
        img_array = np.array(img.convert('RGB'))
        height, width = img_array.shape[:2]

        # Calculate brightness for each pixel (average of RGB)
        brightness = np.mean(img_array, axis=2)

        # Search from bottom up for dark pixels
        left_x, left_y = None, None
        right_x, right_y = None, None
        body_bottom_y = None

        # Start from bottom and work up
        for y in range(height - 1, -1, -1):
            # Check left side (left third of image)
            if left_y is None:
                for x in range(width // 3):
                    if brightness[y, x] < darkness_threshold:
                        left_x, left_y = x, y
                        if body_bottom_y is None:
                            body_bottom_y = y
                        break

            # Check right side (right third of image)
            if right_y is None:
                for x in range(width - 1, 2 * width // 3, -1):
                    if brightness[y, x] < darkness_threshold:
                        right_x, right_y = x, y
                        if body_bottom_y is None:
                            body_bottom_y = y
                        break

            # Stop once we've found both
            if left_y is not None and right_y is not None:
                break

        return (left_x or 0, left_y or height-1,
                right_x or width-1, right_y or height-1,
                body_bottom_y or height-1)

def generate_face_config():
    """Generate face configuration from images in faces/ directory."""
    faces_dir = "faces"
    config = {"faces": []}

    all_faces = []

    # Add the default blank face
    blank_path = "facecam-blank.png"
    if os.path.exists(blank_path):
        width, height = get_image_dimensions(blank_path)
        left_x, left_y, right_x, right_y, body_bottom = find_bottom_dark_pixels(blank_path)

        all_faces.append({
            "id": "blank",
            "name": "Blank Face",
            "image": blank_path,
            "width": width,
            "height": height,
            "body_bottom": body_bottom,
            "left_anchor": (left_x, left_y),
            "right_anchor": (right_x, right_y),
            "targetFrame": {
                "x": 110,
                "y": 80,
                "width": 110,
                "height": 105
            }
        })

        print(f"{blank_path}: {width}x{height}, bottom_y={body_bottom}, anchors=({left_x},{left_y})-({right_x},{right_y})")

    # Process all face images
    if os.path.exists(faces_dir):
        face_files = sorted([f for f in os.listdir(faces_dir)
                           if f.startswith('facecam-') and f.endswith('.png')
                           and not '-blank' in f])

        for filename in face_files:
            filepath = os.path.join(faces_dir, filename)
            width, height = get_image_dimensions(filepath)
            left_x, left_y, right_x, right_y, body_bottom = find_bottom_dark_pixels(filepath)

            # Extract face number from filename
            face_num = filename.replace('facecam-', '').replace('.png', '')

            face_config = {
                "id": f"face-{face_num}",
                "name": f"Face {face_num}",
                "image": f"faces/{filename}",
                "width": width,
                "height": height,
                "body_bottom": body_bottom,
                "left_anchor": (left_x, left_y),
                "right_anchor": (right_x, right_y),
                # Target frame - estimated based on proportions
                "targetFrame": {
                    "x": int(width * 0.35),
                    "y": int(height * 0.31),
                    "width": int(width * 0.35),
                    "height": int(height * 0.41)
                }
            }

            all_faces.append(face_config)
            print(f"{filename}: {width}x{height}, bottom_y={body_bottom}, anchors=({left_x},{left_y})-({right_x},{right_y})")

    # Normalize: find the max body_bottom to use as reference
    if all_faces:
        max_bottom = max(f["body_bottom"] for f in all_faces)
        print(f"\nMax body bottom: {max_bottom}")
        print("All faces will be aligned to this baseline.\n")

        # Add normalization info
        for face in all_faces:
            face["alignment_offset"] = max_bottom - face["body_bottom"]
            config["faces"].append(face)

    # Write to JSON file
    with open('faces-config.json', 'w') as f:
        json.dump(config, f, indent=2)

    print(f"\nGenerated faces-config.json with {len(config['faces'])} faces")
    print("Faces are aligned using bottom-most dark pixels.")

if __name__ == "__main__":
    generate_face_config()
