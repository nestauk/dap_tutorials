
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

PROJECT_DIR = Path(__file__).resolve().parents[1]
SEED = 42

def load_data(input_path = PROJECT_DIR / 'inputs/train.csv', test_size=0.2):
    data = pd.read_csv(input_path)
    
    # Fill missing values
    data['Age'].fillna(data['Age'].mean(), inplace=True)
    data['Embarked'].fillna('S', inplace=True)# Assume they embarked from Southampton if unknown

    # Label encode the categorical columns that are currently strings
    data['Sex'] = LabelEncoder().fit_transform(data['Sex'])
    data['Embarked'] = LabelEncoder().fit_transform(data['Embarked'])

    # Select the features that we will use to predict survival
    features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    target = 'Survived'

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=test_size, random_state=SEED)
    
    return X_train, X_test, y_train, y_test