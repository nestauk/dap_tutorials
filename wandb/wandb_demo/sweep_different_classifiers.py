"""
Runs a sweep across 3 different models and various hyperparameters to find the combination that gives the best accuracy.

The number of hyperparameter combinations tried is controlled by N_RUNS.

The different hyperparameter values to try is controlled by sweep_configuration.
"""

from dotenv import load_dotenv
import pandas as pd
import os
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import wandb

import utils
from utils import PROJECT_DIR, load_data, SEED

load_dotenv()

os.chdir(PROJECT_DIR)

WANDB_PROJ = "Titanic"  # Change this to your project name!
WANDB_USER = os.environ.get("wandb_username")  # Change this to your username!
JOB = "predict survival"

N_RUNS = 5 # How many different hyperparameter combinations to try aka how many different runs

sweep_configuration = {
    'method': 'random',  # Choose from 'grid', 'random', or 'bayes'
    'metric': {
        'name': 'accuracy',
        'goal': 'maximize'   
    },
    'parameters': {
        'model_type': {
            'values': ['logistic_regression', 'svm', 'random_forest']
        },
        'C': {
            'values': [0.01, 0.1, 1]
        },
        'max_iter': {
            'values': [10, 100, 1000]
        },
        'penalty': {
            'values': ['l2', None]
        },
        'solver': {
            'values': ['lbfgs']
        },
        # SVM hyperparams
        'kernel': {
            'values': ['linear', 'rbf']
        },
        'gamma': {
            'values': ['auto']
        },
        # RF hyperparams
        'n_estimators': {
            'values': [10, 100]
        },
        'max_depth': {
            'values': [5, 10, 50]
        },
        'min_samples_split': {
            'values': [2, 5, 10]
        },
        'min_samples_leaf': {
            'values': [1, 2, 4]
        }
    }
}


def train(config, X_train, X_test, y_train, y_test):
    if config.model_type == 'logistic_regression':
        model = LogisticRegression(C=config['C'], max_iter=config['max_iter'],
                                   penalty=config['penalty'], solver=config['solver'], random_state=SEED)
    elif config.model_type == 'svm':
        model = SVC(C=config['C'], kernel=config['kernel'], gamma=config['gamma'], random_state=SEED)
    elif config.model_type == 'random_forest':
        model = RandomForestClassifier(n_estimators=config['n_estimators'], max_depth=config['max_depth'],
                                       min_samples_split=config['min_samples_split'],
                                       min_samples_leaf=config['min_samples_leaf'], random_state=SEED)

    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    cm = confusion_matrix(y_test, preds)
    cm = pd.DataFrame(cm)
    
    return accuracy, cm

def main():
    wandb.init(project=WANDB_PROJ, job_type=JOB, save_code=True)
    X_train, X_test, y_train, y_test = load_data()
    accuracy, cm = train(wandb.config, X_train, X_test, y_train, y_test)
    wandb.log({"accuracy": accuracy})
    
    # Log confusion matrix
    wb_confusion_matrix = wandb.Table(data=cm, columns=["0", "1"])
    wandb.log({"confusion_matrix": wb_confusion_matrix})
    
    wandb.finish()

if __name__ == "__main__":
    sweep_id = wandb.sweep(sweep=sweep_configuration, project=WANDB_PROJ)
    wandb.agent(sweep_id, entity=WANDB_USER, function=main, count=N_RUNS)