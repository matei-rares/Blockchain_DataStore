import numpy as np
import tensorflow as tf
from keras.src.callbacks import EarlyStopping
from ml.Model import Model



# 95%

class ModelYK(Model):
    def __init__(self):
        model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(2,)),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dense(16, activation='relu'),#, kernel_regularizer=tf.keras.regularizers.l2(0.001)),
            # kernel_regularizer=tf.keras.regularizers.l2(0.01)
            # tf.keras.layers.BatchNormalization(),# +1%
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')  # kernel_regularizer=tf.keras.regularizers.l1(0.01) # -1%
        ])
        test="ml/"
        file=test
        super().__init__(model=model,
                         model_save_file_path=file+'years_km.weights.h5',
                         model_train_file_path=file+'years_km_train.weights.h5',
                         features_file_path=file+'features_yk.npy',
                         labels_file_path=file+'labels_yk.npy')

        self.model.compile(optimizer='adam',
                           loss='binary_crossentropy',
                           metrics=['accuracy', 'mse'])

    def train(self, save_model=True, save_set=False, load_set=True):
        features, labels = self.generate_data(load_set)

        split = int(0.8 * len(features))
        train_features, test_features = features[:split], features[split:]
        train_labels, test_labels = labels[:split], labels[split:]

        early_stopping = EarlyStopping(monitor='mse', patience=50, restore_best_weights=True)

        self.model.fit(train_features, train_labels, epochs=100, batch_size=32, validation_split=0.2,
                       callbacks=[early_stopping])
        res = self.model.evaluate(test_features, test_labels)
        print(res)

        km = 18000
        new_fabrication_years = np.array([2010, 2015, 2020, 2000, 1999])
        new_no_km = np.array([15000, km * 8, km * 5, (km - 3000) * 24, 20 * km])

        # new_fabrication_years_normalized = (new_fabrication_years - np.mean(fabrication_years)) / np.std(fabrication_years)
        # new_no_km_normalized = (new_no_km - np.mean(no_km)) / np.std(no_km)
        # new_features = np.column_stack((new_fabrication_years_normalized, new_no_km_normalized))

        new_features = np.column_stack((new_fabrication_years, new_no_km))

        predictions = self.model.predict(new_features)

        for i in range(len(predictions)):
            print("year:", new_fabrication_years[i], "km:", new_no_km[i], "prediction:", predictions[i])

        new_fabrication_years = np.array([2011, 1960])
        new_no_km = np.array([15000, 1152000])

        new_features = np.column_stack((new_fabrication_years, new_no_km))

        predictions = self.model.predict(new_features)

        for i in range(len(predictions)):
            print("year:", new_fabrication_years[i], "km:", new_no_km[i], "prediction:", predictions[i])

        if save_model:
            self.model.save_weights(self.model_train_file_path)
        if save_set:
            np.save(self.features_file_path, features)
            np.save(self.labels_file_path, labels)

        print("-------------------Antrenare terminata-------------------")

    def generate_data(self, load_set=True):
        features = None
        labels = None
        if load_set:
            features = np.load(self.features_file_path)
            labels = np.load(self.labels_file_path)
        else:
            no_samples = 1000
            years = np.random.randint(2000, 2023, size=no_samples)
            kms = np.random.randint(0, 400000, size=no_samples)
            avg_kms = kms / (2024 - years)
            labels = np.where((avg_kms >= 14000) & (avg_kms <= 20000), 0, 1)
            features = np.column_stack((years, kms))
            unique, counts = np.unique(labels, return_counts=True)
            print(dict(zip(unique, counts)))
        # fabrication_years = (fabrication_years - np.mean(fabrication_years)) / np.std(fabrication_years)
        # no_km = (no_km - np.mean(no_km)) / np.std(no_km)

        return features, labels

    def load(self):
        self.model.load_weights(self.model_save_file_path)

    def predict(self,fabrication_year,no_km):
        # new_fabrication_years = np.array([2011, 1960])
        # new_no_km = np.array([15000, 1152000])
        #
        # new_features = np.column_stack((new_fabrication_years, new_no_km))
        new_features=np.column_stack((fabrication_year,no_km))

        predictions = self.model.predict(new_features)
        for i in range(len(predictions)):
            print("year:", fabrication_year, "km:", no_km, "prediction:", predictions[i])
        return str(predictions[0][0])

def tust():
    model = ModelYK()
    #model.train(False,False,False)
    model.load()
    while True:
        model.predict(10000,2019)

#tust()

'''
Epoch 100/100
20/20 ━━━━━━━━━━━━━━━━━━━━ 0s 3ms/step 
- accuracy: 0.8784 - loss: 0.2303 - mse: 0.0756 - val_accuracy: 0.9563 - val_loss: 0.1336 - val_mse: 0.0355

7/7 ━━━━━━━━━━━━━━━━━━━━ 0s 1ms/step - accuracy: 0.9671 - loss: 0.1311 - mse: 0.0346  
[0.15340770781040192, 0.9549999833106995, 0.03860003501176834]
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 61ms/step
year: 2010 km: 15000 prediction: [0.9999866]
year: 2015 km: 144000 prediction: [0.42677322]
year: 2020 km: 90000 prediction: [0.6331048]
year: 2000 km: 360000 prediction: [0.11798751]
year: 1999 km: 360000 prediction: [0.22448269]
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 60ms/step
year: 2011 km: 15000 prediction: [0.9999671]
year: 1960 km: 1152000 prediction: [3.3453423e-07]
'''



