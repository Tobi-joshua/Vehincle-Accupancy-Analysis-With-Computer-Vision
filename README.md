# Vehicle Occupancy Analysis with Computer Vision 🚗📊


This repository contains code for a Streamlit-based application using OpenCV for analyzing vehicle occupancy in video footage. The application detects and tracks vehicles, calculates occupancy times, and generates detailed reports.

# Features

## Vehicle Detection: 🚗
Utilizes YOLO (You Only Look Once) object detection with OpenCV to detect vehicles in video frames.

## Tracking: 🎯
Tracks vehicles across frames to determine entry and exit times.

## Occupancy Calculation: ⏱️
Calculates the duration of vehicle occupancy based on entry and exit times.

## Streamlit Interface: 🖥️
Provides an intuitive web-based interface powered by Streamlit for easy interaction and visualization of results.

## Report Generation: 📊
Generates detailed reports including vehicle IDs, entry times, exit times, and occupancy durations.

# Installation
## Clone the repository:
- git clone https://github.com/yourusername/Vehincle-Accupancy-Analysis-With-Computer-Vision.git
- 
- cd Vehincle-Accupancy-Analysis-With-Computer-Vision

##Install dependencies:
-pip install -r requirements.txt
-
-Run the Streamlit application:

streamlit run app.py
Open a browser and go to http://localhost:8501 to view the application.

# Usage
Upload a video file (supported formats: mp4, mov, avi).
Click "Process Video" to analyze vehicle occupancy.
View the analyzed video with overlaid vehicle tracking.
Download a CSV report containing detailed occupancy data.
Example

Contributing
Contributions are welcome! Please fork the repository and create a pull request with your improvements.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Additional Notes
Ensure your environment has Python 3.10 or above and all dependencies from requirements.txt installed.
Customize and extend the functionality as needed for specific use cases or enhancements.
This README provides a comprehensive overview of your repository, including installation instructions, usage guidelines, and contribution details.
