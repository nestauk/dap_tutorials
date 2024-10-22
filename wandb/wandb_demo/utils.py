import logging
import numpy as np
import os
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from typing import Tuple

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PROJECT_DIR = Path(__file__).resolve().parents[1]
os.chdir(PROJECT_DIR)
SEED = 42

np.random.seed(SEED)

def load_data(input_path: Path = PROJECT_DIR / 'inputs/train.csv', test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Load and do some basic preprocessing on the Titanic training data.
    
    This function reads data from a CSV file, handles missing values, encodes categorical variables,
    and splits the data into training and testing datasets.

    Args:
        input_path (Path, optional): Path to the CSV file containing the dataset.
                                     Defaults to PROJECT_DIR/'inputs/train.csv'.
        test_size (float, optional): The proportion of the dataset to include in the test split.
                                     Defaults to 0.2.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: A tuple containing the training
        and testing datasets for the features and target variable.
    """
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