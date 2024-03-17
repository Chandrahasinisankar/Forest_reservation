import cv2

# Load pre-trained cascade classifier for pedestrian detection
pedestrian_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')

# Function to detect pedestrians in the frame
def detect_pedestrians(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pedestrians = pedestrian_cascade.detectMultiScale(gray, 1.1, 4)
    return pedestrians

# Function to draw rectangles around detected pedestrians
def draw_rectangles(frame, detections, color):
    for (x, y, w, h) in detections:
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

# Main function to process the video feed
def main():
    cap = cv2.VideoCapture(0)  # Initialize webcam feed

    while True:
        ret, frame = cap.read()  # Read a frame from the webcam feed

        if not ret:
            break

        pedestrians = detect_pedestrians(frame)

        # Draw rectangles around detected pedestrians
        draw_rectangles(frame, pedestrians, (0, 255, 0))  # Green for pedestrians

        # Count the number of pedestrians
        num_pedestrians = len(pedestrians)
        cv2.putText(frame, f'Pedestrians: {num_pedestrians}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Crowd Monitoring', frame)

        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
