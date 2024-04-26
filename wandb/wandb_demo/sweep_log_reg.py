from dotenv import load_dotenv
import logging
import numpy as np
import os
import pandas as pd
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import wandb

import utils
from utils import PROJECT_DIR, load_data, SEED

load_dotenv()

os.chdir(PROJECT_DIR)

WANDB_PROJ = "Titanic" # Change this to your project name!
WANDB_USER = os.environ.get("wandb_username") # Change this to your username!
JOB = "predict survival"

N_RUNS = 5 # How many different hyperparameter combinations to try aka how many different runs

sweep_configuration = {
    'method': 'random',  # grid, random, or bayes. Random picks random combinations of hyperparameter values. Grid picks all possible combinations. Bayes picks based on past results.
    'metric': {
      'name': 'accuracy',
      'goal': 'maximize'   
    },
    'parameters': {
        'penalty': {'values': ['l2', None]},
        'solver': {'values': ['lbfgs']}, # even if there are hyperparameters that you aren't planning on varying, it is still good to record these!
        'C': {
            'values': [0.01, 0.1, 1]
        },
        'max_iter': {
            'values': [10, 100, 500]
        }
    }
}


def train(config, X_train, X_test, y_train, y_test):
    # Build the model
    model = LogisticRegression(C=config['C'],
                               max_iter=config['max_iter'],
                               penalty = config['penalty'],
                               random_state=SEED,
                               solver = config['solver'])
    model.fit(X_train, y_train)

    # Predict and evaluate
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    
    cm = confusion_matrix(y_test, preds)
    cm = pd.DataFrame(cm)
    
    return accuracy, cm

def main():
    wandb.init(project=WANDB_PROJ,
               job_type=JOB,
               save_code=True,
               tags=["logistic regression"])
    X_train, X_test, y_train, y_test = load_data()
    accuracy, cm = train(wandb.config,  X_train, X_test, y_train, y_test)
    wandb.log({"accuracy": accuracy})
    
    # Log confusion matrix
    wb_confusion_matrix = wandb.Table(data=cm, columns=["0", "1"])
    wandb.log({"confusion_matrix": wb_confusion_matrix})

if __name__ == "__main__":
    
    sweep_id = wandb.sweep(sweep=sweep_configuration, project=WANDB_PROJ)

    wandb.agent(sweep_id, entity=WANDB_USER, function=main,
                count=N_RUNS
                )