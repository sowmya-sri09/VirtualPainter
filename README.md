🖌️ Virtual Painter – Gesture-Based Creative Tool
A real-time AI-powered virtual painting app where your hand is the brush! Built using OpenCV, MediaPipe, and Python, this project allows users to draw, erase, switch colors, draw shapes, and even save their canvas — using nothing but gestures and voice commands.
 ✨ Features
- ✋ Hand tracking using MediaPipe
- 🎨 Drawing & erasing with finger gestures
- 🎙️ Voice command integration (e.g. "red", "save", "circle")
- 🔷 Shape tools (circle, rectangle)
- 💾 Canvas saving as image
📂 How to Run
bash
conda create -n painter_env python=3.9
conda activate painter_env
pip install opencv-python mediapipe numpy speechrecognition pyaudio
python main.py
