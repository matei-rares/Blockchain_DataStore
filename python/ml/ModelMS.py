import numpy as np
import tensorflow as tf

from ml.Model import Model


# bazat pe anul de fabricatie si pe ultimul an de revizie si itp pot sa fac un if pentru a verifica daca e la zi cu chestiile legale
# prima data se face la 3 ani, daca are intre 3 si 12 ani se face la 2 ani,daca are mai mult de 12 se face la un an

# daune tehnice ascunse - ascuns 10
# pasibil de probleme tehnice viitoare - pasibil 01

# 3. sells>0.2(o data la 5 ani) -> 10
# 4. mentenanta>2 -> 01
# 5. mentenanta<0.5 -> 10


# 94%
class ModelMS(Model):
    def __init__(self):
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(2,)),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(2, activation='sigmoid')  # kernel_regularizer=tf.keras.regularizers.l1(0.01) # -1%
        ])

        super().__init__(model=model,
                         model_save_file_path='ml/men_sel.weights.h5',
                         model_train_file_path='ml/men_sel_train.weights.h5',
                         features_file_path='ml/features_ms.npy',
                         labels_file_path='ml/labels_ms.npy')

        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', 'mse'])

    def train(self, save_model=False, save_set=False, load_set=True):
        n_params = 2
        if load_set:
            features = np.load('features_ms.npy')
            labels = np.load('labels_ms.npy')
            split = int(0.8 * len(features))
        else:
            dataset = self.generate_data(2000)
            split = int(0.8 * len(dataset))
            features = np.array(dataset)[:, :n_params]
            labels = np.array(dataset)[:, n_params:]

        train_features, test_features = features[:split], features[split:]
        train_labels, test_labels = labels[:split], labels[split:]

        manual_test = np.array([[2, 0.2],  # 00
                                [1.9, 0.2],

                                [1, 1.2],  # 10
                                [2, 0.9],

                                [2.2, 0.2],  # 01

                                [0.2, 0.2],  # 10
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

        self.model.fit(train_features, train_labels, epochs=100, batch_size=32,
                       validation_split=0.2)  # ,validation_data=(test_features, test_labels))# callbacks=[early_stopping])

        res = self.model.evaluate(test_features, test_labels)
        print(res)

        predictions = self.model.predict(manual_test)
        print(predictions)

        rounded_predictions = np.round(predictions)
        print(rounded_predictions)

        self.model.save_weights("men_sel_train.weights.h5")
        np.save('features_ms.npy', features)
        np.save('labels_ms.npy', labels)
        if save_model:
            self.model.save_weights(self.model_train_file_path)
        if save_set:
            np.save(self.features_file_path, features)
            np.save(self.labels_file_path, labels)

        print("-------------------Antrenare terminata-------------------")

    def generate_data(self, num_samples=2000):

        dataset = []
        for _ in range(num_samples):
            param1 = np.random.uniform(0, 3)
            param2 = np.random.uniform(0, 1)
            label1 = 0
            label2 = 0
            if param1 > 2:
                label2 = 1
            elif param1 < 0.5:
                label1 = 1
            if param2 > 0.2:
                label1 = 1
            dataset.append([param1, param2, label1, label2])
        return dataset

    def load(self):
        self.model.load_weights(self.model_save_file_path)

        pass

    def predict(self, mentenances, sells):
        # mentenances=1
        # sells=0.2
        new_features = np.column_stack((mentenances, sells))
        predictions = self.model.predict(new_features)
        for i in range(len(predictions)):
            print("Nr mentenante:", mentenances, " nr vaznari:", sells, " predictie:", predictions[i])
        return [str(predictions[0][0]) , str(predictions[0][1]) ]


def tust():
    model = ModelMS()
    #model.train(False,False,False)
    model.load()
    while True:
        model.predict()

# tust()

'''
    76/76 ━━━━━━━━━━━━━━━━━━━━ 0s 2ms/step - accuracy: 0.9419 - loss: 0.1198 - mse: 0.0375 - val_accuracy: 0.9290 - val_loss: 0.0576 - val_mse: 0.0137
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 54ms/step
[[3.6997938e-01 4.5592737e-01]
 [3.8954261e-01 2.3971057e-01]
 [1.0000000e+00 6.5248183e-05]
 [1.0000000e+00 5.2711248e-01]
 [3.3649457e-01 8.5664827e-01]
 [9.6415597e-01 3.0241097e-08]]
[[0. 0.]
 [0. 0.]
 [1. 0.]
 [1. 1.]
 [0. 1.]
 [1. 0.]]
'''
