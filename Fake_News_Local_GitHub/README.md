# Fake News Detection System — Local Flask Version

This version is set up to run on your Windows computer with Python/VS Code. Online-hosting configuration has not been included. It supports news text classification, image text extraction using Tesseract OCR, and a dataset preview page.

## Project files

```text
Fake_News_Local_GitHub/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── coda_text.csv
└── templates/
    ├── index.html
    └── dataset.html
```

## 1. Requirements

- Python 3.10 or 3.11 is recommended.
- Internet access on first launch so Transformers can download the model.
- Tesseract OCR is required only for image uploads. Install Tesseract OCR for Windows and keep its default path (`C:\Program Files\Tesseract-OCR\tesseract.exe`), or set the `TESSERACT_CMD` environment variable to its actual executable path.

## 2. Run locally in Windows PowerShell

Open PowerShell in this project folder and run:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in your browser. The first start may take a few minutes while the model downloads. Keep the terminal open while using the site. Stop the server with `Ctrl+C`.

If installing PyTorch fails, use the install command recommended by the official PyTorch selector for your operating system, then run `pip install -r requirements.txt` again.

## 3. Push to GitHub

Create an empty repository on GitHub. In this project folder, run:

```powershell
git init
git add .
git commit -m "Prepare local fake news detection app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the URL with your repository URL. The `.gitignore` excludes virtual environments and downloaded model caches. The CSV is included because the dataset page uses it.

## Notes

- This is a local development server, not a public production server.
- `pytesseract` is a Python wrapper; Tesseract OCR itself must also be installed separately for image text extraction.
- The prediction is a model estimate, not proof that a news story is true or false.
- The included `coda_text.csv` has no known FAKE/REAL label column, so it is displayed as a dataset preview and is not used to train this model.
