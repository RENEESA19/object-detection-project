from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_potholes(frame):
    results = model(frame)
    boxes = results[0].boxes
    
    pothole_count = len(boxes)
    annotated_frame = results[0].plot()
    
    return annotated_frame, pothole_count
