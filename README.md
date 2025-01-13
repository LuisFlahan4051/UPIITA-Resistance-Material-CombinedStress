## Windows:

```
.\.venv\Scripts\activate
pip install -r requirements.txt
python .\main.py

pyinstaller --onefile -w main.py
```

## Linux:

```
source .venv/bin/activate
pip install -r requirements.txt
python .\main.py
```

## Generate requirements:

```
pip freeze > requirements.txt
```

## Install requirements:

```
pip install -r requirements.txt
```

## ForRegen requeriments used in the project:

```
pip freeze > requirements.txt
```
