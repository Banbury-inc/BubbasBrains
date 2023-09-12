import Metashape
import cv2  # Import OpenCV

# Initialize Metashape document
doc = Metashape.app.document

# Initialize the video capture from the USB webcam
cap = cv2.VideoCapture(0)  # 0 corresponds to the default webcam

if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit()

# Create a new chunk
chunk = doc.addChunk()

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        print("Error: Unable to capture a frame from the webcam.")
        break

    # Convert the frame to a Metashape image and add it to the chunk
    image = Metashape.Photo()
    image.open(BytesIO(cv2.imencode('.jpg', frame)[1].tobytes()))
    chunk.addPhotos([image])

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV window
cap.release()
cv2.destroyAllWindows()

# Set up alignment, dense cloud generation, and other Metashape tasks here as needed
