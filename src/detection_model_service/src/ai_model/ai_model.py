from PIL import Image
from ultralytics import YOLO
import torch
import numpy as np


class CustomDetectionModel:
    def __init__(self, weights_path: str, class_dict:dict, model_type: str = "YOLO", conf: int = 0.6):
        if model_type == "YOLO":
            self.model = YOLO(weights_path)
            self.model_type = model_type
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.conf = conf
            self.class_dict = class_dict
        else:
            raise Exception(f"Model type '{model_type}' is not supported.")

    def format_output(self, model_results):
        #     results = [
        #         {
        #             "class_id": 1,
        #              "x1_coord": 0.51,
        #              "y1_coord": 0.51,
        #              "x2_coord": 0.52,
        #              "y2_coord": 0.52,
        #              "x3_coord": 0.53,
        #              "y3_coord": 0.53,
        #              "x4_coord": 0.54,
        #              "y4_coord": 0.54,
        #              "probability": 0.82
        #         },
        #         { ... },
        #         ...
        #     ]
        results = []
        if self.model_type == "YOLO":

            classes = [int(elem) for elem in model_results[0].obb.cls.tolist()]
            probs = [round(elem, 3) for elem in model_results[0].obb.conf.tolist()]
            obbs = model_results[0].obb.xyxyxyxyn

            for i in range(len(classes)):
                results.append({
                    "class_name": self.class_dict[classes[i]],
                    "x1_coord": np.clip(obbs[i][0][0].item(), 0, 1),
                    "y1_coord": np.clip(obbs[i][0][1].item(), 0, 1),
                    "x2_coord": np.clip(obbs[i][1][0].item(), 0, 1),
                    "y2_coord": np.clip(obbs[i][1][1].item(), 0, 1),
                    "x3_coord": np.clip(obbs[i][2][0].item(), 0, 1),
                    "y3_coord": np.clip(obbs[i][2][1].item(), 0, 1),
                    "x4_coord": np.clip(obbs[i][3][0].item(), 0, 1),
                    "y4_coord": np.clip(obbs[i][3][1].item(), 0, 1),
                    "probability": probs[i]
                })
        else:
            raise Exception(f"Format output for model type '{self.model_type}' is not supported.")

        return results

    def predict(self, image: Image):
        res = self.model(image, conf=self.conf, device=self.device)

        return self.format_output(res)


primitive_classes_inv = {"cone": 0, "cube": 1, "cylinder": 2, "sphere": 3, "torus": 4}
primitive_classes = {0: "cone", 1: "cube", 2: "cylinder", 3: "sphere", 4: "torus"}

path = r"model_weights/yolov11m_obb_best.pt"
detection_model = CustomDetectionModel(weights_path=path, class_dict=primitive_classes)

async def process(image: bytes) -> list[dict]:
    return detection_model.predict(image)
