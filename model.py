'''

Last Modified: 2025-02-27
Author: Vishesh

'''

from sklearn.linear_model import LogisticRegression
import pandas as pd


data = pd.read_excel('data.xlsx')
X = data.drop('Target', axis=1)
y = data['Target']

model = LogisticRegression()

model.fit(X, y)

print('Model trained successfully!')



#saving the encoder and model

import pickle

def save_trained_model(model, filename='model.pkl'):
    """
    Save the trained model and associated metadata
    """
    model_data = {
        'model': model
    }

    with open(filename, 'wb') as file:
        pickle.dump(model_data, file)
    print(f"Model saved successfully to {filename}")

# Save the model
save_trained_model(model)