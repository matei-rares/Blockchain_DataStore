import numpy as np
import tensorflow as tf
from ml.Model import Model


# bazat pe anul de fabricatie si pe ultimul an de revizie si itp pot sa fac un if pentru a verifica daca e la zi cu chestiile legale
# prima data se face la 3 ani, daca are intre 3 si 12 ani se face la 2 ani,daca are mai mult de 12 se face la un an

# daune majore - majore 10
# daune tehnice ascunse - ascuns 01


# 1. crash>1  -> 11
# 2. damages>3 -> 10
# 3. services - (crash + damage) > 2 -> 01
# 4. crash > services -> 10
# 5. damages > services -> 01
# crash,damage,service

# 84%
class ModelCDS(Model):
    def __init__(self):
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(3,)),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(2, activation='sigmoid')
        ])

        super().__init__(model=model,
                         model_save_file_path='ml/crash_dam_ser.weights.h5',
                         model_train_file_path='ml/crash_dam_ser_train.weights.h5',
                         features_file_path='ml/features_cds.npy',
                         labels_file_path='ml/labels_cds.npy')

        self.model.compile(optimizer='adam', loss="binary_crossentropy", metrics=['accuracy', 'mse'])

    def train(self, save_model=False, save_set=False, load_set=True):
        n_params = 3
        n_outputs = 2
        split = 0
        if load_set:
            features = np.load(self.features_file_path)
            labels = np.load(self.labels_file_path)
            split = int(0.8 * len(features))
        else:
            dataset = self.generate_data(2000)
            split = int(0.8 * len(dataset))
            # train_features = np.array(dataset)[:, :n_params]
            # train_labels = np.array(dataset)[:, n_params:]
            features = np.array(dataset)[:, :n_params]
            labels = np.array(dataset)[:, n_params:]

        train_features, test_features = features[:split], features[split:]
        train_labels, test_labels = labels[:split], labels[split:]


        zero = 0
        one = 0
        two = 0
        three = 0
        for i in train_labels:
            if i[0] == 0 and i[1] == 0:
                zero += 1
            elif i[0] == 0 and i[1] == 1:
                one += 1
            elif i[0] == 1 and i[1] == 0:
                two += 1
            elif i[0] == 1 and i[1] == 1:
                three += 1
        print(zero, one, two, three)

        manual_tests = np.array([[0.1, 1, 2],  # 00
                                 [1.1, 1, 2],  # 11
                                 [0.9, 3.1, 5],  # 10
                                 [0.9, 2, 5],  # 01
                                 [0.9, 0, 0.8],  # 10
                                 [0.8, 1.1, 0.9],  # 01
                                 ])

        dataset_test = [
            [1, 0, 0, 0],
            [2, 0.19, 0, 0],
            [2, 0.19, 0, 0],
            [2, 0.2, 0, 0],  # 3
            [2, 0.21, 1, 0],
            [2, 0.25, 1, 0],
            [2, 0.29, 1, 0],
            [1, 0.21, 1, 0],
            [1, 0.21, 1, 0],
            [1, 0.21, 1, 0],
            [1, 0.21, 1, 0],
            [1, 0.21, 1, 0],
            [1, 0.21, 1, 0],
            [1, 0.21, 1, 0],
            [2, 0.2, 0, 0],  # 4
            [2.1, 0.2, 0, 1],
            [2.2, 0.2, 0, 1],
            [2.3, 0.2, 0, 1],
            [2.4, 0.2, 0, 1],
            [2.5, 0.2, 0, 1],
            [2.1, 0, 0, 1],
            [2.1, 0, 0, 1],
            [5, 0.2, 0, 0],  # 5
            [4, 0.2, 1, 0],
            [3, 0.2, 1, 0],
            [2, 0.2, 1, 0],
            [1, 0.2, 1, 0],
            [0, 0.2, 1, 0],
            [0.4, 0, 1, 0],
        ]

        # validation_split este ignorat daca se da validation_data
        # todo nu mai pune validation_data ci doar validation split, si fa evaluate cu test_features si test_labels dupa antrenare

        self.model.fit(train_features, train_labels, epochs=100, batch_size=32,validation_split=0.2)  # ,validation_data=(test_features, test_labels))# callbacks=[early_stopping])

        res = self.model.evaluate(test_features, test_labels)
        print(res)

        predictions = self.model.predict(manual_tests)
        print(predictions)

        rounded_predictions = np.round(predictions)
        print(rounded_predictions)

        if save_model:
            self.model.save_weights(self.model_train_file_path)
        if save_set:
            np.save(self.features_file_path, features)
            np.save(self.labels_file_path, labels)

        print("-------------------Antrenare terminata-------------------")

    def generate_data(self, num_samples=2000):
        dataset = []
        for _ in range(num_samples):
            crashes = np.random.uniform(0, 2)
            damages = np.random.uniform(0, 5)
            services = np.random.uniform(0, 8)
            label1 = 0
            label2 = 0
            if crashes > 1:
                label1 = 1
                label2 = 1
            elif damages > 3:
                label1 = 1
            elif services - (crashes + damages) > 2:
                label2 = 1
            if crashes > services:
                label1 = 1
            elif damages > services:
                label2 = 1
            dataset.append([crashes, damages, services, label1, label2])
        return dataset

    def load(self):
        self.model.load_weights(self.model_save_file_path)

    def predict(self, crashes, damages, services):
        # crashes=0.1
        # damages=1
        # services=2
        new_features = np.column_stack((crashes, damages, services))
        predictions = self.model.predict(new_features)
        for i in range(len(predictions)):
            print("No crashes:", crashes, ", no damages:", damages, ", no services:", services, ", prediction:",
                  predictions[i])
        return [str(predictions[0][0]), str(predictions[0][1])]

    def see_metrics(self,trained_model=False, load_set=True):
        n_params = 3
        n_outputs = 2
        split = 0
        if load_set:
            features = np.load(self.features_file_path)
            labels = np.load(self.labels_file_path)
            split = int(0.8 * len(features))
        else:
            dataset = self.generate_data(2000)
            split = int(0.8 * len(dataset))
            # train_features = np.array(dataset)[:, :n_params]
            # train_labels = np.array(dataset)[:, n_params:]
            features = np.array(dataset)[:, :n_params]
            labels = np.array(dataset)[:, n_params:]
        print(features)
        print(labels)
        train_features, test_features = features[:split], features[split:]
        train_labels, test_labels = labels[:split], labels[split:]
        if trained_model:
            self.model.load_weights(self.model_train_file_path)
        else:
            self.load()
        res = self.model.evaluate(test_features, test_labels)
        print(res)


def tust():
    model = ModelCDS()
    #model.see_metrics(True,True)
    model.train(save_model=False, save_set=False, load_set=False)
    # while True:
    #     model.predict()

#tust()

"""
ultima executie
51/51 ━━━━━━━━━━━━━━━━━━━━ 0s 2ms/step - accuracy: 0.8421 - loss: 0.0496 - mse: 0.0140 - val_accuracy: 0.8300 - val_loss: 0.0502 - val_mse: 0.0155
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 54ms/step
[[1.2824518e-07 8.1228102e-03]
 [8.9463890e-01 7.1749604e-01]
 [7.7217293e-01 3.5318356e-02]
 [1.3615978e-03 6.2915695e-01]
 [9.8659909e-01 1.7111978e-02]
 [1.5383044e-04 9.1185451e-01]]
[[0. 0.]
 [1. 1.]
 [1. 0.]
 [0. 1.]
 [1. 0.]
 [0. 1.]]

"""
