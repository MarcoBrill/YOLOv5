import cv2
import torch
from pathlib import Path

# Load YOLOv5 model from Ultralytics
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # You can use 'yolov5m', 'yolov5l', or 'yolov5x' for larger models

def detect_objects_in_video(video_path, output_path):
    """
    Detects objects in a video and saves the output video with bounding boxes.

    Args:
        video_path (str): Path to the input video file.
        output_path (str): Path to save the output video file.
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Perform object detection
        results = model(frame)

        # Render bounding boxes on the frame
        rendered_frame = results.render()[0]

        # Write the frame with bounding boxes to the output video
        out.write(rendered_frame)

    # Release resources
    cap.release()
    out.release()
    print(f"Output video saved to {output_path}")

if __name__ == "__main__":
    # Define input and output paths
    input_video = "input_video.mp4"  # Replace with your input video path
    output_video = "output_video.mp4"  # Replace with your desired output video path

    # Run object detection
    detect_objects_in_video(input_video, output_video)
