from pathlib import Path


from sorawm.utils.video_utils import VideoLoader
from ultralytics import YOLO
import numpy as np
from sorawm.configs import WATER_MARK_DETECT_YOLO_WEIGHTS


# based on the sora tempalte to detect the whole, and then got the icon part area.

model = YOLO(WATER_MARK_DETECT_YOLO_WEIGHTS)
model.eval()

results = model("resources/first_frame.png")  # Predict on an image

print(results)