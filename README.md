# This repo used for backend challange

## What stack are we using
1. Flask
2. RestX
3. Marsmallow
4. Sqlalchemy
5. MySql
6. and many more supporting library

## Requirements

1. Python 3.8
2. MySql
3. Virtualenv
4. I recommend to using python `pip`

## How to run this project

```
git clone https://github.com/rizperdana/flask-rest-mysql.git
```

Since we using isolated environment here (virtualenv), make sure to install it in your python library. After that make sure you setup the `.env` files before running this script, the default value could be find on `.env.example` files one, or you can just copy paste config below:

```
DEBUG=True
FLASK_ENV=development
FLASK_APP=app.py
DATABASE_URI='mysql://user:password@localhost:3306/db-name'
HOST=localhost
PORT=5555
```

After that we can start our app by running this command:

```
flask shell
```

```
flask start
```
