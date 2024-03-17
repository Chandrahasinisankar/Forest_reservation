from email.mime.application import MIMEApplication
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from scrp import detect_objects, get_location_info, extract_exif_tags
import os

def format_detected_objects(detected_objects_result):
    object_counts = {}
    for obj in detected_objects_result:
        if obj in object_counts:
            object_counts[obj] += 1
        else:
            object_counts[obj] = 1
    
    formatted_objects = []
    for obj, count in object_counts.items():
        formatted_objects.append(f"{obj} - {count}")
    
    return "\n".join(formatted_objects)

def format_location_info(location_info_result):
    latitude, longitude, address = location_info_result
    return f"Latitude: {latitude}\nLongitude: {longitude}\nAddress: {address}"

def format_exif_tags(exif_tags):
    return "\n".join(f"{tag}: {value}" for tag, value in exif_tags.items())

def send_email(subject, body, to_email, app_password, attachment_path):
    email = 'sankarchandrahasini@gmail.com'  # Update with your email
    message = MIMEMultipart()
    message['From'] = email
    message['To'] = to_email
    message['Subject'] = subject

    detected_objects_result = detect_objects(attachment_path)
    location_info_result = get_location_info(attachment_path)
    exif_tags = extract_exif_tags(attachment_path)

    email_body = "Detected Objects:\n"
    email_body += format_detected_objects(detected_objects_result)
    
    if location_info_result:
        email_body += "\n\nLocation Information:\n"
        email_body += format_location_info(location_info_result)

    if exif_tags:
        email_body += "\n\nEXIF Tags:\n"
        email_body += format_exif_tags(exif_tags)

    message.attach(MIMEText(email_body, 'plain'))

    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            message.attach(part)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()

        try:
            server.ehlo()
            server.login(email, app_password)
            server.sendmail(email, to_email, message.as_string())
            print(f"Email sent to {to_email} successfully.")
        
        except smtplib.SMTPException as e:
            print(f"SMTP Exception: {e}")

if __name__ == "__main__":
    app_password = "iyyz zjym xvib cygy"  # Update with your app password
    subject = "scrapped information"
    body = ""  # Leave body empty for now
    recipient_email = "chandrahasinis.csbs2022@citchennai.net"
    attachment_path = input(r"Enter the path to the image file: ")  # Make sure this points to an image file
    send_email(subject, body, recipient_email, app_password, attachment_path)
#chandrahasinis.csbs2022@citchennai.net