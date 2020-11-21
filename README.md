# petrepo
pet application backend repository


## Get started
### I) First run :
1. Pull the repo
2. First, create a database then change the informations on config.py according to this:
```python
  app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://[USERNAME]:[PASSWORD]@localhost/[DATABASE NAME]"
```

3. Create a python virtual environnement in the repo :
(please use the version noted in the file `.python_version`)
```bash
$ python3.8 -m venv venv38 # or name it whatever you want 
```
4. Activate the venv:
(change the directory if you named it something else than venv38)
```bash
$ source venv38/bin/activate
```
*or*
```bash
$ . venv38/bin/activate
```
If this step works, the name of your venv will be prepended between parenthesis to your terminal prompt

5. install the requirements
```bash
$ pip install -r requirements.txt
```
6. Create the tables :  
  * Run the python REPL in the base directory:
```bash
$ python
```
  * In the python REPL execute the following lines: 
```python
>>> from models import db
>>> create_all()
```
7. Start the server
```bash
$ python run.py
```

### II) Subsequent runs
In future runs, to enter the venv and start the server in one command:
if you chose another name for your venv, change it in `go.sh` before sourcing it :
```bash
$ . go.sh
```
If everything goes well your server should be online and you get prompted the address (most probably `http://127.0.0.1:5000/` if you didn't change the port in config.py ) 
### III) Endpoint testing
We have a postman export in the file  `pet app.postman_collection.json`,  just import it and you will be able to test the API endpoints

after that, follow steps for flask rest api on this link:
https://www.codementor.io/@dongido/how-to-build-restful-apis-with-python-and-flask-12qto530jd
