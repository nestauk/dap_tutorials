"""
Runs a dummy classifier that predicts survival based on the survival rate in the training data.
Logs this as a run on wandb, including accuracy and a confusion matrix.
"""
from dotenv import load_dotenv
import logging
import numpy as np
import os
import pandas as pd
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix
import wandb

import utils
from utils import PROJECT_DIR, load_data

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