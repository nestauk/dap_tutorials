"""
Runs a logistic regression to predict survival.
Logs this as a run on wandb, including accuracy and a confusion matrix.
"""
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

if __name__ == "__main__":

    # # Split the data
    X_train, X_test, y_train, y_test = load_data()
    
    run = wandb.init(
        project=WANDB_PROJ,
        job_type=JOB,
        save_code=True,
        tags=["logistic regression"],
    )
    
    log_reg_config = {'penalty': 'l2',
                  'C': 1.0,
                  'random_state': SEED,
                  'solver':'lbfgs',
                  'max_iter':100}
    
    model = LogisticRegression(penalty=log_reg_config['penalty'],
                           C=log_reg_config['C'],
                           solver=log_reg_config['solver'],
                           max_iter=log_reg_config['max_iter'],
                           random_state=log_reg_config['random_state'])
    model.fit(X_train, y_train)

    # Predict and evaluate
    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    logging.info(f"Accuracy: {accuracy}")

    wandb.run.summary["accuracy"] = accuracy

    cm = confusion_matrix(y_test, preds)
    cm = pd.DataFrame(cm)
    logging.info(f"Confusion matrix:\n{cm}")

    # Log confusion matrix
    wb_confusion_matrix = wandb.Table(data=cm, columns=["0", "1"])
    run.log({"confusion_matrix": wb_confusion_matrix})

    # End the weights and biases run
    wandb.finish()