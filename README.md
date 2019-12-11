## 1. What is Property-based testing or random testing?
PBT is a black-box testing technique, which generates random inputs to test whether a function verifies a property.

More info: https://en.wikipedia.org/wiki/Random_testing

The PBT implementation I've used is [Hypothesis](https://hypothesis.readthedocs.io/en/latest/).

## 2. Requeriments to run the code
This should work in any machine with =<python3.6.

I've tested it with python3.7 and pip3.

### Using a virtual enviroment
In order to isolate the dependencies, you should use [virtualenv](https://docs.python-guide.org/dev/virtualenvs/) to avoid any cross dependency issue.

Then you can create a virtualenv with: ```virtualenv -p python3 venv/```

Activate it with: ```source venv/bin/activate```

Finally, you can install the dependencies with : ```pip install -r requirements.txt```

## 3. How to run tests?
If you want to run poker tests, then use: ```python3 -m src.poker.test.poker_test```

Otherwise run it as a normal script, e.g. ```python3 src/stateful_testing/die_hard.py```
