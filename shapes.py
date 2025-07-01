# shapes.py
import cv2

def draw_shape(img, shape, start_point, end_point, color, thickness):
    if shape == "rectangle":
        cv2.rectangle(img, start_point, end_point, color, thickness)
    elif shape == "circle":
        center = (int((start_point[0] + end_point[0]) / 2), int((start_point[1] + end_point[1]) / 2))
        radius = int(((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)**0.5 / 2)
        cv2.circle(img, center, radius, color, thickness)
