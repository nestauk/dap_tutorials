
# 🧪 Unit testing tutorial 🧪

Create the environment

```
cd dap_tutorials/unit_tests
conda create --name unit_tests python=3.10
conda activate unit_tests
pip install -r requirements.txt
```

Run the tests for the basic functions in the terminal by running:

```
pytest tests/test_basic_functions.py

```

Did you get any errors? Edit `basic_functions.py` until the tests run.

Test the more complex functions by running:

```
pytest tests/test_complex_functions.py
```

Did one take more time than the other?


You can also run all the tests in the tests folder by simply running:
```
pytest

```




