# UPIITA Resistance Material - Combined Stress

This application was developed as a project in a materials mechanics subject at UPIITA-IPN, Qt technology is used in Python for the development of the UI and implementation of Plotly to display more sophisticated graphics.

## 🎥 Demo:

[![Demo](screenshots/demo.png)](https://youtu.be/y4GYawCsVuc)

## 📸 Screenshots

![screenshot1](screenshots/1.png)

![screenshot2](screenshots/2.png)

![screenshot3](screenshots/3.png)

![screenshot4](screenshots/4.png)

![screenshot5](screenshots/5.png)

## 🚀 Installation and Setup

### Windows:

```bash
.\.venv\Scripts\activate
pip install -r requirements.txt
python .\main.py

pyinstaller --onefile -w main.py
```

### Linux:

```bash
sudo dnf install python3-virtualenv python3-devel gcc gcc-c++ make
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python .\main.py
```

## 📦 Dependency Management

### Generate requirements:

```bash
pip freeze > requirements.txt
```

### Install requirements:

```bash
pip install -r requirements.txt
```
