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


class CustomMultiClassificationModel:
    def __init__(self, weights_paths: dict, input_size: int, hidden_size: int, num_layers: int,
                 class_dicts: dict[str: dict], scene_class_dict: dict, scene_class_dict_inv: dict,
                 primitive_class_dict: dict, primitive_class_dict_inv: dict):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"CLASSIFICATION device: {self.device}")
        self.models = {key: GRUClassifier(input_size=input_size,
                                          hidden_size=hidden_size,
                                          num_layers=num_layers,
                                          num_classes=2,
                                          device=self.device).to(self.device)
                       for key in weights_paths
                       }
        for key, model in self.models.items():
            model.load_state_dict(torch.load(weights_paths[key]))

        self.class_dicts = class_dicts

        self.scene_class_dict = scene_class_dict
        self.scene_class_dict_inv = scene_class_dict_inv
        self.primitive_class_dict = primitive_class_dict
        self.primitive_class_dict_inv = primitive_class_dict_inv

    def format_output(self, model_result: dict) -> dict:
        # in
        # {'office_model': tensor([[-2.6277, -0.0750]], device='cuda:0'),
        # 'livingroom_model': tensor([[-0.2540, -1.4948]], device='cuda:0'),
        # 'warehouse_model': tensor([[-1.4678, -0.2619]], device='cuda:0'),
        # 'greenhouse_model': tensor([[-2.9719, -0.0526]], device='cuda:0')}

        classes = {}
        class_probs = []

        i = 0
        for key, value in model_result.items():
            classes[i] = key.split("_")[0]
            class_probs.append(value.tolist()[0][0])
            i += 1

        class_probs = nnf.softmax(torch.Tensor(class_probs), dim=0)
        top_p, top_class = class_probs.topk(1, dim=0)
        class_probs = [round(el, 3) for el in class_probs.tolist()]

        return {
            "top_class_ind": top_class.item(),
            "top_class_name": classes[top_class.item()],
            "classes": classes,
            "class_probs": class_probs
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
        models_res = {key: model(seq_input) for key, model in self.models.items()}

        return self.format_output(models_res)


scene_classes_inv = {"office": 0, "livingroom": 1, "warehouse": 2, "greenhouse": 3}
scene_classes = {0: "office", 1: "livingroom", 2: "warehouse", 3: "greenhouse"}

primitive_classes_inv = {"cone": 0, "cube": 1, "cylinder": 2, "sphere": 3, "torus": 4}
primitive_classes = {0: "cone", 1: "cube", 2: "cylinder", 3: "sphere", 4: "torus"}

class_dicts = {"office_model": {0: "office", 1: "not_office"},
               "livingroom_model": {0: "livingroom", 1: "not_livingroom"},
               "warehouse_model": {0: "warehouse", 1: "not_warehouse"},
               "greenhouse_model": {0: "greenhouse", 1: "not_greenhouse"}}

weights_paths = {"office_model": r"model_weights/gru_model_office_0750_accuracy_on_test_50epochs.pt",
                "livingroom_model": r"model_weights/gru_model_livingroom_0625_accuracy_on_test_60epochs.pt",
                "warehouse_model": r"model_weights/gru_model_warehouse_0875_accuracy_on_test_39epochs.pt",
                "greenhouse_model": r"model_weights/gru_model_greenhouse_1000_accuracy_on_test_150epochs.pt"}

input_size = 12
hidden_size = 32
num_layers=10

classification_model = CustomMultiClassificationModel(weights_paths=weights_paths,
                                                      input_size=input_size,
                                                      hidden_size=hidden_size,
                                                      num_layers=num_layers,
                                                      class_dicts=class_dicts,
                                                      scene_class_dict=scene_classes,
                                                      scene_class_dict_inv=scene_classes_inv,
                                                      primitive_class_dict=primitive_classes,
                                                      primitive_class_dict_inv=primitive_classes_inv)


async def process(detected_primitives: list[dict]) -> dict:
    return classification_model.predict(detected_primitives)
