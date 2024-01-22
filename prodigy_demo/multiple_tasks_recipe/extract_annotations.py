import sys
import json
from prodigy.components.db import connect

db = connect()
# This is a list of dictionaries that one can modify and export
data = db.get_dataset(sys.argv[1])

unnecessary_variables = ["text", "meta", "tokens", "options", "_input_hash", "_task_hash", "_session_id", "_view_id", "config"]
# remove unecessary variables
for s in data:
    for var in unnecessary_variables:
        s.pop(var, None)

with open(sys.argv[2], "w") as outfile:
    json.dump(data, outfile)
