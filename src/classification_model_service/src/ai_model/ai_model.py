import torch
from torch import nn
import torch.nn.functional as nnf
from torch.nn.utils.rnn import pad_packed_sequence, PackedSequence, pack_sequence


class GRUClassifier(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes, device, bidirectional=False, dropout=0):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.h_layers_multiplier = 1
        self.device = device
        if bidirectional:
            self.h_layers_multiplier = 2

        # layers
        self.gru = nn.GRU(input_size=input_size,
                          hidden_size=hidden_size,
                          num_layers=num_layers,
                          dropout=dropout,
                          bidirectional=bidirectional)
        self.fc = nn.Linear(hidden_size * self.h_layers_multiplier, num_classes)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, x: PackedSequence, *args):
        # Set initial hidden and cell states - GRU
        h0 = torch.zeros(self.num_layers * self.h_layers_multiplier,
                         x.batch_sizes.max(),
                         self.hidden_size).to(self.device)

        # Forward propagate RNN
        out, _ = self.gru(x, h0)
        out, sizes = pad_packed_sequence(out)
        out = torch.stack([out[size - 1][i] for i, size in enumerate(sizes)])
        # Decode the hidden state of the last time step
        out = self.fc(out)

        out = self.softmax(out)
        return out


class CustomClassificationModel:
    def __init__(self, weights_path: str, input_size: int, hidden_size: int, num_layers: int, num_classes: int,
                 scene_class_dict: dict, scene_class_dict_inv: dict,
                 primitive_class_dict: dict, primitive_class_dict_inv: dict):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"CLASSIFICATION device: {self.device}")
        self.model = GRUClassifier(input_size=input_size,
                                   hidden_size=hidden_size,
                                   num_layers=num_layers,
                                   num_classes=num_classes,
                                   device=self.device).to(self.device)
        self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
        self.scene_class_dict = scene_class_dict
        self.scene_class_dict_inv = scene_class_dict_inv
        self.primitive_class_dict = primitive_class_dict
        self.primitive_class_dict_inv = primitive_class_dict_inv

    def format_output(self, model_result: list, class_dict: dict) -> dict:
        prob = nnf.softmax(model_result, dim=1)
        top_p, top_class = prob.topk(1, dim=1)

        prob = [round(el, 3) for el in prob.tolist()[0]]

        return {
            "top_class_ind": top_class.item(),
            "top_class_name": class_dict[top_class.item()],
            "classes": class_dict,
            "class_probs": prob
        }

    def format_input(self, primitives: list[dict]) -> PackedSequence:
        # columns = ["primitive_class_0", "primitive_class_1", "primitive_class_2", "primitive_class_3",
        #            "x1", "y1", "x2", "y2", "x3", "y3", "x4", "y4"]

        rows = []
        for primitive in primitives:
            class_id = self.primitive_class_dict_inv[primitive["class_name"]]
            # custom one_hot_encoding
            rows.append([int(class_id == 0),
                         int(class_id == 1),
                         int(class_id == 2),
                         int(class_id == 3),
                         float(primitive["x1_coord"]),
                         float(primitive["y1_coord"]),
                         float(primitive["x2_coord"]),
                         float(primitive["y2_coord"]),
                         float(primitive["x3_coord"]),
                         float(primitive["y3_coord"]),
                         float(primitive["x4_coord"]),
                         float(primitive["y4_coord"])])

        items = torch.tensor(rows, dtype=torch.float32)
        seq = pack_sequence([items], enforce_sorted=False).to(self.device)

        return seq

    def predict(self, primitives: list[dict]):
        seq_input = self.format_input(primitives)
        res = self.model(seq_input)

        return self.format_output(res, self.scene_class_dict)


c_weights_path = "model_weights/best_gru_model_0700_accuracy_on_val_145epochs.pt"
input_size = 12
hidden_size = 32
num_layers = 10
num_classes = 4

scene_classes_inv = {"office": 0, "livingroom": 1, "warehouse": 2, "greenhouse": 3}
scene_classes = {0: "office", 1: "livingroom", 2: "warehouse", 3: "greenhouse"}
primitive_classes_inv = {"cone": 0, "cube": 1, "cylinder": 2, "sphere": 3, "torus": 4}
primitive_classes = {0: "cone", 1: "cube", 2: "cylinder", 3: "sphere", 4: "torus"}

classification_model = CustomClassificationModel(weights_path=c_weights_path,
                                                 input_size=input_size,
                                                 hidden_size=hidden_size,
                                                 num_layers=num_layers,
                                                 num_classes=num_classes,
                                                 scene_class_dict=scene_classes,
                                                 scene_class_dict_inv=scene_classes_inv,
                                                 primitive_class_dict=primitive_classes,
                                                 primitive_class_dict_inv=primitive_classes_inv)


async def process(detected_primitives: list[dict]) -> dict:
    return classification_model.predict(detected_primitives)
