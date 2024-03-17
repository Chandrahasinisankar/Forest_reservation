

import cv2
import numpy as np
from PIL import Image
import PIL
from geopy.geocoders import Nominatim
from PIL import Image, ExifTags
import pyttsx3

def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal_degrees = degrees + minutes/60 + seconds/3600
    if direction in ['S', 'W']:
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def detect_objects(image_path):
    # Load YOLO
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getUnconnectedOutLayersNames()

    # Load image using the absolute path
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image from {image_path}")
        exit()

    height, width, _ = image.shape

    # Preprocess image
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(layer_names)

    # Get bounding boxes, confidences, and class ids
    confidences = []
    class_ids = []
    boxes = []
    detected_objects = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                detected_objects.append(classes[class_id])

    return detected_objects

def get_location_info(image_path):
    img = Image.open(image_path)
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
    }

    gps_info = exif.get('GPSInfo')

    if gps_info:
        for tag_id, value in gps_info.items():
            tag_name = PIL.ExifTags.GPSTAGS.get(tag_id, tag_id)
            if tag_name == 'GPSLatitude':
                latitude = dms_to_decimal(*value, gps_info.get('GPSLatitudeRef', 'N'))
            elif tag_name == 'GPSLongitude':
                longitude = dms_to_decimal(*value, gps_info.get('GPSLongitudeRef', 'E'))

                # Reverse geocode coordinates to obtain address
                geolocator = Nominatim(user_agent="image_metadata_script")
                location = geolocator.reverse((latitude, longitude), language='en')
                address = location.address

                return latitude, longitude, address

def extract_exif_tags(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()

        if exif_data is not None:
            exif_tags = {ExifTags.TAGS[key]: exif_data[key] for key in exif_data.keys() if key in ExifTags.TAGS}
            return exif_tags
        else:
            print("No EXIF data found in the image.")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def main(image_path):
    detected_objects_result = detect_objects(image_path)
    location_info_result = get_location_info(image_path)
    exif_tags = extract_exif_tags(image_path)

    return detected_objects_result, location_info_result, exif_tags