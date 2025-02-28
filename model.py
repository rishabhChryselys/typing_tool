'''

Last Modified: 2025-02-27
Author: Vishesh

'''

# Importing the required libraries
from sklearn.linear_model import LogisticRegression
import numpy as np
from sklearn.model_selection import GridSearchCV
import pandas as pd


data = pd.read_excel('data.xlsx')
X = data.drop('Target', axis=1)
y = data['Target']

param_grid_lr = {
    'C': np.logspace(-3, 3, 7),
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear']
}

# Initialize GridSearchCV
grid_search_lr = GridSearchCV(LogisticRegression(random_state=42), 
                             param_grid_lr, cv=3, scoring='accuracy')

# Fit the model
grid_search_lr.fit(X, y)

# Get the best model
best_lr = grid_search_lr.best_estimator_

print('Model trained successfully!')



#saving the encoder and model

import pickle

def save_trained_model(model, filename='model.pkl'):
    """
    Save the trained model and associated metadata
    """
    model_data = model

    with open(filename, 'wb') as file:
        pickle.dump(model_data, file)
    print(f"Model saved successfully to {filename}")

# Save the model
save_trained_model(best_lr)