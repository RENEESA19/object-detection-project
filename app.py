import streamlit as st
import cv2
import numpy as np
from utils import detect_potholes
import tempfile

st.set_page_config(page_title="Pothole Detection", layout="wide")

st.title("🚧 AI Road Pothole Detection System")

option = st.sidebar.selectbox(
    "Choose Input Type",
    ["Image", "Video", "Webcam"]
)

# ---------------- IMAGE ----------------
if option == "Image":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)

        result, count = detect_potholes(image)

        st.image(result, channels="BGR")
        st.success(f"Detected Potholes: {count}")

# ---------------- VIDEO ----------------
elif option == "Video":
    uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi"])

    if uploaded_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())

        cap = cv2.VideoCapture(tfile.name)

        stframe = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            result, count = detect_potholes(frame)

            stframe.image(result, channels="BGR")

        cap.release()

# ---------------- WEBCAM ----------------
elif option == "Webcam":
    run = st.checkbox("Start Webcam")

    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    while run:
        ret, frame = cap.read()
        if not ret:
            break

        result, count = detect_potholes(frame)

        stframe.image(result, channels="BGR")

    cap.release()
