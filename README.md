# README for Algorithm and Machine Learning Practice Repository

## Overview

This repository is a comprehensive suite for practicing and honing skills in algorithms and machine learning, with a specific focus on data preparation, data gathering, and data processing. The exercises contained herein are designed to provide hands-on experience and challenge individuals to apply their knowledge in a practical setting.

The repository is structured to facilitate incremental learning, with each exercise building upon the principles covered in the previous ones. It is ideal for individuals looking to improve their understanding of algorithmic problem solving and data manipulation techniques used in the field of machine learning.

## Contents

- `root/`: Contains exercise files and their corresponding unit tests.
- `test/`: Includes test suites to validate the solutions provided in the exercises.
- `img/`: Stores image files used in the README and documentation.
- `note/`: Contains notes and additional information related to the exercises.
- `*.py`: Python script files containing algorithm and machine learning exercises.

## Getting Started

The command `python3 -m unittest discover test` does not require any extra libraries outside of the standard Python distribution. The `unittest` module is part of the Python Standard Library, which comes pre-installed with Python.

### Prerequisites

- Python 3.6 or higher. If you don't have Python installed, you can download it from [python.org](https://www.python.org/downloads/).

### Setting Up a Virtual Environment

It is recommended to set up a virtual environment to manage dependencies and avoid conflicts with system-wide Python packages.

1. To create a virtual environment, run:

    ```bash
    python3 -m venv venv
    ```

2. To activate the virtual environment:
   - On macOS and Linux:

    ```bash
    source venv/bin/activate
    ```

   - On Windows:

    ```bash
    .\venv\Scripts\activate
    ```

### Running the Code

1. To execute an exercise script, run:

   ```bash
   python3 exercises/ex_<number>.py
   ```

   Replace `<number>` with the exercise number you wish to run.

### Writing Tests

1. Tests are written using Python's built-in `unittest` framework.
2. To create a new test, add a class in the `test/` directory extending `unittest.TestCase`.
3. Define test methods within this class, and use assertions to validate your code's behavior.

### Running Tests

1. To run a specific test file, execute the following command:

   ```bash
   python3 -m unittest test/ex_<number>_test.py
   ```

   Replace `<number>` with the test number you wish to run.

2. To run all tests in the repository, execute:

   ```bash
   python3 -m unittest discover -s test -p "*_test.py"
   ```

hihi
