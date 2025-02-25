from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
import pandas as pd

questions = ['Q1', 'Q3', 'Q4', 'Q5_1', 'Q5_2', 'Q5_3', 'Q5_4', 'Q7']
data = pd.read_excel('data.xlsx')
X = data[questions]
y = data['Target']
onehot = OneHotEncoder()
X_hot = onehot.fit_transform(X).toarray()
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

model = LogisticRegression()

model.fit(X_hot, y)

print('Model trained successfully!')



#saving the encoder and model

import pickle

def save_trained_model(model, label_encoder, questions,one_hot_encoder, filename='model.pkl'):
    """
    Save the trained model and associated metadata
    """
    model_data = {
        'model': model,
        'label_encoder': label_encoder,
        'questions': questions,
        'one_hot_encoder': one_hot_encoder
    }

    with open(filename, 'wb') as file:
        pickle.dump(model_data, file)
    print(f"Model saved successfully to {filename}")

# Save the model
save_trained_model(model, label_encoder, questions,onehot)