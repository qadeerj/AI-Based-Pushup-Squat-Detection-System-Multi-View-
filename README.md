---
title: AI Multi-View Pushup & Squat Detection System
author: Muhammad Qadeer
Date: 12/2/2026
---


# AI Multi-View Pushup & Squat Detection System


## Overview


This project is a real-time AI-based exercise detection system built using Python, OpenCV, and MediaPipe Pose. The system processes video input and detects and counts Pushups and Squats across multiple camera angles including Side View, Front View, Back View, and Diagonal View.


It uses human pose estimation and dynamic joint angle calculations to track exercise movements and repetition counts.


---


## Features


- Multi-view camera detection  
- Automatic visible-side selection  
- Real-time Pushup and Squat repetition counting  
- Elbow, Body Alignment, and Knee angle calculation  
- Angle smoothing to reduce jitter  
- Stage-based motion tracking (Up / Down logic)  
- Skeleton overlay visualization  
- Live joint angle debugging  
- Processing progress indicator  
- Output video generation with counters  


---


## Technical Approach


### Pose Estimation


MediaPipe Pose extracts 33 body landmarks per frame including:


- Shoulder  
- Elbow  
- Wrist  
- Hip  
- Knee  
- Ankle  


Each landmark provides x, y, z coordinates and visibility confidence.


---


### Pushup Detection Logic


- Elbow Angle (Shoulder → Elbow → Wrist)  
- Body Alignment Angle (Shoulder → Hip → Ankle)  
- Shoulder vertical movement (for front/back views)  
- Multi-view adaptive logic  
- Stage-based transition logic to prevent double counting  


---


### Squat Detection Logic


- Knee Angle (Hip → Knee → Ankle)  
- Smoothed angle tracking using rolling buffer  
- Adaptive threshold-based stage detection  
- State-based repetition counting  


---
### Installation
```bash
pip install opencv-python mediapipe numpy
```
### Run the Project
```bash
python exercise_detection.py
```
### Debug Information Displayed
- Elbow Angle
- Body Angle
- Knee Angle
- View Type (Side / Front / Back)
- Pushup & Squat Counters
- Processing Progress (%)

### Applications
- AI Personal Trainer Systems
- Fitness Analytics Platforms
- Computer Vision Portfolio Projects
- Human Motion Analysis
- Health & Sports Monitoring

### Future Improvements
- Form correctness scoring
- Additional exercises (Lunges, Plank, Jump Squats)
- Real-time webcam version
- Streamlit web interface
= ML-based automatic exercise classification

### Conclusion

This project demonstrates practical implementation of pose estimation, multi-view adaptive logic, and rule-based motion analysis for real-time exercise tracking. It serves as a strong portfolio project for computer vision and AI-based fitness applications.
