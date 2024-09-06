# multiple model using gridsearchCV
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense
from keras import backend as K
import tensorflow as tf
import tf.keras.wrappers.scikit_learn.KerasRegressor

# Load your data
df = pd.read_csv('result.csv')

# Select features and target variables
X = df[['Freq', 'Height', 'Permitivity', 'loss']]  
Y_x = df['Cut_x']
Y_y = df['Cut_y']

# Split the data into training and test sets
X_train, X_test, Y_x_train, Y_x_test = train_test_split(X, Y_x, test_size=0.3, random_state=42)
_, _, Y_y_train, Y_y_test = train_test_split(X, Y_y, test_size=0.3, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define RMSE metric
def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true)))

# Function to create model
def create_model(optimizer='adam'):
    model = Sequential()
    model.add(Dense(8, input_dim=X_train.shape[1], activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['mae', rmse])
    return model

# Wrap the model using the custom KerasRegressor
model = KerasRegressor(build_fn=create_model)

# Define the grid search parameters
param_grid = {
    'batch_size': [20, 40, 60, 80],
    'epochs': [1500, 2500, 3500, 4500, 5500],
    'optimizer': ['adam']
}

# Grid search for Cut_x
grid_x = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, scoring='neg_mean_squared_error')
grid_x_result = grid_x.fit(X_train, Y_x_train)

# Summarize results for Cut_x
print(f"Best for Cut_x: {grid_x_result.best_score_} using {grid_x_result.best_params_}")

# -------------------------------------------------------------------------------------------------

# Grid search for Cut_y
grid_y = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, scoring='neg_mean_squared_error')
grid_y_result = grid_y.fit(X_train, Y_y_train)

# Summarize results for Cut_y
print(f"Best for Cut_y: {grid_y_result.best_score_} using {grid_y_result.best_params_}")

# Evaluate the best model for Cut_x
best_model_x = grid_x_result.best_estimator_.model
loss_x, mae_x, rmse_x = best_model_x.evaluate(X_test, Y_x_test)
print(f"Model for Cut_x - Loss (MSE): {loss_x}, MAE: {mae_x}, RMSE: {rmse_x}")

# Evaluate the best model for Cut_y
best_model_y = grid_y_result.best_estimator_.model
loss_y, mae_y, rmse_y = best_model_y.evaluate(X_test, Y_y_test)
print(f"Model for Cut_y - Loss (MSE): {loss_y}, MAE: {mae_y}, RMSE: {rmse_y}")

# Save the best models
best_model_x.save('best_model_x.keras')
best_model_y.save('best_model_y.keras')