import logging
import numpy as np
import pandas as pd
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import wandb

from utils import PROJECT_DIR, load_data

WANDB_PROJ = "Titanic" # Change this to your project name!
WANDB_USER = "rosie-oxbury" # Change this to your username!
JOB = "predict survival"
SEED = 42

np.random.seed(SEED)

# PROJECT_DIR = Path(__file__).resolve().parents[1]

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    
    # data = pd.read_csv(PROJECT_DIR / 'inputs/train.csv')
    
    # # Fill missing values
    # data['Age'].fillna(data['Age'].mean(), inplace=True)
    # data['Embarked'].fillna('S', inplace=True)# Assume they embarked from Southampton if unknown

    # # Label encode the categorical columns that are currently strings
    # data['Sex'] = LabelEncoder().fit_transform(data['Sex'])
    # data['Embarked'] = LabelEncoder().fit_transform(data['Embarked'])

    # # Select the features that we will use to predict survival
    # features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    # target = 'Survived'

    # # Split the data
    X_train, X_test, y_train, y_test = load_data()
    
    run = wandb.init(
        project=WANDB_PROJ,
        job_type=JOB,
        save_code=True,
        tags=["baseline_model"],
    )

    survival_rate = y_train.value_counts(normalize=True)[1]

    y_pred_baseline = np.random.binomial(1, survival_rate, len(y_test))

    wandb.run.summary["accuracy"] = accuracy_score(y_test, y_pred_baseline)

    cm = confusion_matrix(y_test, y_pred_baseline)
    cm = pd.DataFrame(cm)
    logging.info(f"Confusion matrix:\n{cm}")

    # Log confusion matrix
    wb_confusion_matrix = wandb.Table(data=cm, columns=["0", "1"])
    run.log({"confusion_matrix": wb_confusion_matrix})

    # End the weights and biases run
    wandb.finish()