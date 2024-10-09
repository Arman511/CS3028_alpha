# CS3028_alpha

## Contents

1. [Project Overview](#project-overview)
2. [Setup Instructions](#setup-instructions)
3. [How to Run](#how-to-run)

## Project Overview

This project is part of the CS3028 course. It includes various scripts and modules to demonstrate different aspects of the course material.

## Setup Instructions

1. Clone the repository to your local machine.
2. Create a virtual environment:
    ```
    python3 -m venv venv
    ```
3. Activate the virtual environment:
    - On macOS/Linux:
        ```
        source venv/bin/activate
        ```
    - On Windows(powershell):
        ```
        .\venv\Scripts\activate.ps1
        ```
4. Install packages
    ``` 
    pip3 install -r ./requirements.txt
    ```

## How to Run

-   To run the project, execute the following command:

    -   On macOS/Linux:
        ```
        ./run
        ```
    -   On Windows(powershell):
        ```
        .\run.ps1
        ```

-   To run the production version, use the following command:
    ```
    gunicorn --config gunicorn_config.py app:app
    ```
