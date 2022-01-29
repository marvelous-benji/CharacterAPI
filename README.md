# CharacterAPI



---

### Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)

---

## Description

A Simple API for interacting with the Lord of the Ring API

#### Technologies

- Python
- Flask
- JWT
- AWS Lambda
- Zappa

[Back To The Top](#read-me-template)

---

## How To Use

[Documentation]( https://pmmo57o8ta.execute-api.us-east-2.amazonaws.com/dev)

#### Installation
```bash
git clone https://github.com/marvelous-benji/CharacterAPI.git
run cd CharacterAPI
setup a virtual enviroment by running python -m venv env
then run source env/bin/activate
finally run pip install -r requirements.txt
(check to see if any of these differ on windows OS)
```


#### SetUp

```python
    For Unix(that is mac or linux)
    You can either export the following configurations or create  a config.json file and enter:
    {
    "SECRET_KEY":{Your Secret Key},
    "FLASK_CONFIG":{Set development or production},
    "API_KEY":{Register an account on the API_URL link to get this},
    "API_URL":"https://the-one-api.dev/v2",
    "DB_DEV_URL":"dev.sqlite",
    "DB_PROD_URL":"prod.sqlite",
    "DB_TEST_URL":"tests.sqlite",
    "DOCS_URL":"https://documenter.getpostman.com/view/15462060/UVeCQ8dj"
    }

    To run test
    pytest -v

    for windows OS use set instead of export

```