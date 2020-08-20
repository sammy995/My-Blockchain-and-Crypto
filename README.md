**Create and Activate virtual environment**
```
py -m venv env-name   
.\env-name\Scripts\activate
```
for Windows OS


**Install all packages**

```
pip install -r requirements.txt
```

**Execute files from moudules**
```
py .\backend\blockchain\block.py
py -m backend.blockchain.block
```  
-For specifying moules in other directories

**Run the Tests**
Activate virtual environment
```
py -m pytest backend/tests
```
all tests should be in tests folder

**To create a package, create a directory with an __init__.py file. Python will then recognize the directory as a package, allowing you to import modules contained in that package with a dot syntax.**

**Run the application and API**

Make sure to activate the virtual environment.
```
py -m backend.app
```
**Running a PEER instance**
Make sure to activate the virtual environment.
path only for local
```
export PEER=True && py -m backend.app

```

**Run the frontend**
In frontend directory:
```
npm run start
```

**Seed backend with data**
Make sure to activate the virtual environment.
```
export SEED_DATA=True && py -m backend.app
```

