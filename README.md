# Django Project

This is a Django project designed to manage team. Below, you'll find information on how to set up and run the project, as well as some additional resources.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Requirements

asgiref==3.8.1
crispy-bootstrap4==2024.1
Django==4.2.13
django-appconf==1.0.6
django-crispy-forms==2.1
django-select2==8.1.2
flake8==7.0.0
isort==5.13.2
mccabe==0.7.0
pycodestyle==2.11.1
pyflakes==3.2.0
sqlparse==0.5.0
typing_extensions==4.11.0


## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/dvkim28/task_management.git
    cd task_management
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```sh
    python manage.py migrate
    ```

5. Create a superuser to access the admin interface:

    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```sh
    python manage.py runserver
    ```

## Usage

- Access the admin interface at `http://127.0.0.1:8000/admin/` and log in with the superuser credentials you created.
- Access the main application at `http://127.0.0.1:8000/`.

## Running Tests

To run tests for the project, use the following command:

```sh
python manage.py test