from abc import ABC, abstractmethod


class Model(ABC):
    def __init__(self, model, model_save_file_path, model_train_file_path, features_file_path, labels_file_path):
        self.model = model
        self.model_save_file_path = model_save_file_path
        self.model_train_file_path = model_train_file_path
        self.features_file_path = features_file_path
        self.labels_file_path = labels_file_path

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def generate_data(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def predict(self, *args):
        pass
