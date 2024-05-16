import cv2

# Load Cascade for face, eye, and mouth
face_cascade = cv2.CascadeClassifier('haar-cascade-files\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haar-cascade-files\haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('haar-cascade-files\haarcascade_mcs_mouth.xml')

# Function to detect face
def detect_face(gray_frame):
    # Detecting face
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

# Function to detect eye
def detect_eye(gray_frame):
    # Detecting eye
    eyes = eye_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return eyes

# Function to detect mouth
def detect_mouth(gray_frame, face_roi):
    # Detecting mouth within the face region
    mouths = mouth_cascade.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return mouths

# Initializing the video capture
cap = cv2.VideoCapture(0)

while True:
    # Read the frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect face
    faces = detect_face(gray_frame)

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        face_roi_gray = gray_frame[y:y + h, x:x + w]
        face_roi_color = frame[y:y + h, x:x + w]

        # Detect eyes within the face region
        eyes = detect_eye(face_roi_gray)

        # Draw rectangles around detected eyes
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(face_roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        # Detect mouth within the face region
        mouths = detect_mouth(face_roi_gray, face_roi_gray)

        # Draw rectangles around detected mouths
        for (mx, my, mw, mh) in mouths:
            cv2.rectangle(face_roi_color, (mx, my), (mx + mw, my + mh), (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Face and Mouth Detection', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
