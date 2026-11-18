
from ultralytics import YOLO
import cv2
import time

from src.quality_controller import (
    get_material_group,
    check_contamination
)


class WasteSortingSystem:

    def __init__(
        self,
        detection_model,
        segmentation_model
    ):

        self.detector = YOLO(detection_model)
        self.segmenter = YOLO(segmentation_model)


    def analyze(
        self,
        image_path,
        expected_material="plastic",
        confidence=0.25
    ):

        start_time = time.time()

        # -----------------------
        # Object Detection
        # -----------------------

        det_result = self.detector.predict(
            source=image_path,
            conf=confidence,
            imgsz=640,
            verbose=False
        )[0]

        detections = []

        if det_result.boxes is not None:

            for box in det_result.boxes:

                class_id = int(box.cls[0].item())

                class_name = det_result.names[
                    class_id
                ]

                conf = float(
                    box.conf[0].item()
                )

                detections.append({
                    "class": class_name,
                    "material":
                        get_material_group(
                            class_name
                        ),
                    "confidence": conf
                })

        # -----------------------
        # Contamination
        # -----------------------

        contaminated, contaminants = (
            check_contamination(
                detections,
                expected_material
            )
        )

        # -----------------------
        # Segmentation
        # -----------------------

        seg_result = self.segmenter.predict(
            source=image_path,
            conf=confidence,
            imgsz=640,
            verbose=False
        )[0]

        segmented_image = seg_result.plot(
            boxes=True,
            masks=True,
            labels=True
        )

        segmented_image = cv2.cvtColor(
            segmented_image,
            cv2.COLOR_BGR2RGB
        )

        processing_time = (
            time.time() - start_time
        )

        return {
            "detections": detections,

            "object_count":
                len(detections),

            "contaminated":
                contaminated,

            "contaminants":
                contaminants,

            "segmented_image":
                segmented_image,

            "processing_time":
                processing_time
        }
