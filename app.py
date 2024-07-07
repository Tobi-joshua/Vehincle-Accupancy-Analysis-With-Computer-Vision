import os
import cv2
import numpy as np
import pandas as pd
import streamlit as st
from datetime import date
import urllib.request


# Function to download YOLO files
def download_yolo_files():
    yolo_weights_url = "https://pjreddie.com/media/files/yolov3.weights"
    yolo_cfg_url = "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg"

    if not os.path.exists("yolov3.weights"):
        with st.spinner('Downloading YOLO weights...'):
            urllib.request.urlretrieve(yolo_weights_url, "yolov3.weights")

    if not os.path.exists("yolov3.cfg"):
        with st.spinner('Downloading YOLO config...'):
            urllib.request.urlretrieve(yolo_cfg_url, "yolov3.cfg")


# Download YOLO files
download_yolo_files()

# Create 'uploads' directory if it doesn't exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Load YOLO model
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Dictionary to hold vehicle times
vehicle_times = {}


# Function to detect vehicles in a frame
def detect_vehicles(frame):
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for output in outs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 2:  # Class 2 is for "car" in COCO dataset
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    vehicles = []

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            vehicles.append((x, y, w, h))

    return vehicles


# Function to track vehicles
def detect_and_track_vehicles(frame, frame_id):
    detected_vehicles = detect_vehicles(frame)

    for vehicle in detected_vehicles:
        if vehicle not in vehicle_times:
            vehicle_times[vehicle] = {'entry': frame_id, 'exit': None}
        else:
            vehicle_times[vehicle]['exit'] = frame_id


# Function to process video
def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    global vehicle_times
    vehicle_times = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_id = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        detect_and_track_vehicles(frame, frame_id)

    cap.release()


# Function to generate report
def generate_report():
    data = []
    frame_rate = 30  # Assuming 30 FPS

    for vehicle, times in vehicle_times.items():
        entry_time = times['entry']
        exit_time = times['exit'] if times['exit'] else entry_time  # Use entry time if still present
        occupancy_time = (exit_time - entry_time) / frame_rate
        data.append([vehicle, entry_time, exit_time, occupancy_time])

    df = pd.DataFrame(data, columns=['Vehicle', 'Entry Time', 'Exit Time', 'Occupancy Time'])
    return df


# Streamlit interface
st.title("Vehicle Occupancy Analysis 🚗📊")

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    video_path = os.path.join("uploads", uploaded_file.name)
    with open(video_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.video(video_path)

    if st.button("Process Video"):
        with st.spinner('Processing video...'):
            process_video(video_path)
            df = generate_report()

            if not df.empty:
                st.dataframe(df)

                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV 📥",
                    data=csv,
                    file_name='occupancy_report.csv',
                    mime='text/csv',
                )
            else:
                st.warning("No vehicles detected in the video.")

        # Debugging output
        st.text(f"Detected Vehicles: {len(vehicle_times)}")
        st.text(f"Vehicle Times: {vehicle_times}")

# Footer with your name and current date
footer = """
<footer style="position: fixed; left: 0; bottom: 0; width: 100%; background-color: #f0f0f0; text-align: center; padding: 10px;">
    <p>Done by Joshua Samuel | {}</p>
</footer>
""".format(date.today().strftime("%B %d, %Y"))

st.markdown(footer, unsafe_allow_html=True)