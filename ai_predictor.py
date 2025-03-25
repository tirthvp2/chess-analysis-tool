# ai_predictor.py
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os


class AIPredictor:
    def __init__(self, model_path="models/outcome_model.keras", encoder_path="models/label_encoder.pkl"):
        self.model_path = model_path
        self.encoder_path = encoder_path
        self.model = None
        self.label_encoder = None

    def load_data(self, dataset_path="data/chess_dataset.csv"):
        """Load and preprocess the dataset."""
        df = pd.read_csv(dataset_path)
        X = df.drop("outcome", axis=1).values
        y = df["outcome"].values

        # Encode outcomes (-1, 0, 1) to (0, 1, 2)
        self.label_encoder = LabelEncoder()
        y = self.label_encoder.fit_transform(y + 1)  # Shift -1,0,1 to 0,1,2

        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def build_model(self, input_shape):
        """Build the neural network model."""
        self.model = tf.keras.Sequential([
            tf.keras.layers.Dense(512, activation="relu", input_shape=input_shape),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(256, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(3, activation="softmax")  # 3 classes: win, draw, loss
        ])
        self.model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        return self.model

    def train(self, X_train, y_train, X_test, y_test, epochs=50, batch_size=64):
        """Train the model and save it."""
        self.model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batch_size)
        self.model.save(self.model_path)
        # Save the label encoder
        joblib.dump(self.label_encoder, self.encoder_path)
        print(f"Model saved to {self.model_path}")
        print(f"Label encoder saved to {self.encoder_path}")

    def load_model(self):
        """Load the trained model."""
        self.model = tf.keras.models.load_model(self.model_path)
        # Load the label encoder
        if os.path.exists(self.encoder_path):
            self.label_encoder = joblib.load(self.encoder_path)
        else:
            raise FileNotFoundError(f"Label encoder not found at {self.encoder_path}. Please train the model first.")

    def predict(self, board_matrix):
        """Predict the outcome for a given board position."""
        if self.model is None:
            self.load_model()
        if self.label_encoder is None:
            self.load_model()  # Ensure label_encoder is loaded
        # Flatten the board matrix and reshape for prediction
        input_data = board_matrix.flatten().reshape(1, -1)
        prediction = self.model.predict(input_data)
        predicted_class = np.argmax(prediction, axis=1)
        probabilities = prediction[0]
        outcome = self.label_encoder.inverse_transform(predicted_class)[0] - 1  # Shift back to -1,0,1
        return outcome, probabilities


if __name__ == "__main__":
    predictor = AIPredictor()
    X_train, X_test, y_train, y_test = predictor.load_data()
    predictor.build_model(input_shape=(X_train.shape[1],))
    predictor.train(X_train, y_train, X_test, y_test)
