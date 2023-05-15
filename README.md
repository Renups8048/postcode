
# Uk Post code validator

Basic Django restful Api to test the given post code is valid or not.
ANd needs to change the format of the post code.

## Installation/Running
These steps explain how to run the code locally and interact with API's. 

- Clone the repository

    ```bash
    git clone git@github.com:Renups8048/postcode.git
    ```

- Activate your desired virtual environment

- Install dependencies by running ```pip install -r requirements.txt``` in the project folder.

- Run your code with `python manage.py runserver`

## Testing
- For validating API  run `http://127.0.0.1:8000/api/validate/?postcode=SW1A2WS`
- For Formating API run `http://127.0.0.1:8000/api/format/?postcode=SW1A2WS`