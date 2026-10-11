from pathlib import Path
import os
import shutil

from flask import Flask, render_template, request
from transformers import pipeline
import pandas as pd
from PIL import Image
import pytesseract

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB image upload limit

# Optional: set TESSERACT_CMD if Tesseract is installed in a non-standard location.
# Windows default is commonly C:\\Program Files\\Tesseract-OCR\\tesseract.exe.
tesseract_override = os.environ.get('TESSERACT_CMD')
if tesseract_override:
    pytesseract.pytesseract.tesseract_cmd = tesseract_override
elif os.name == 'nt':
    windows_tesseract = Path(r'C:\Program Files\Tesseract-OCR\tesseract.exe')
    if windows_tesseract.exists():
        pytesseract.pytesseract.tesseract_cmd = str(windows_tesseract)
    elif shutil.which('tesseract'):
        pytesseract.pytesseract.tesseract_cmd = shutil.which('tesseract')

MODEL_NAME = 'jy46604790/Fake-News-Bert-Detect'
print('Loading AI model. First launch can take a few minutes...')
classifier = pipeline('text-classification', model=MODEL_NAME, tokenizer=MODEL_NAME)
print('AI model loaded successfully.')


def normalize_result(result):
    label = str(result['label']).upper()
    confidence = float(result['score']) * 100
    if label == 'LABEL_0':
        prediction = 'FAKE NEWS'
    elif label == 'LABEL_1':
        prediction = 'REAL NEWS'
    else:
        prediction = label
    return prediction, confidence


def predict_news(text):
    result = classifier(text, truncation=True, max_length=512)[0]
    return normalize_result(result)


@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = None
    news_text = ''
    extracted_text = ''
    error = None

    if request.method == 'POST':
        news_text = request.form.get('news_text', '').strip()
        image_file = request.files.get('news_image')

        try:
            if image_file and image_file.filename:
                try:
                    image = Image.open(image_file.stream).convert('RGB')
                    extracted_text = pytesseract.image_to_string(image).strip()
                except pytesseract.TesseractNotFoundError:
                    error = ('Tesseract OCR was not found. Install Tesseract OCR and '
                             'restart the app. See README.md for instructions.')
                except Exception as exc:
                    error = f'Could not read the uploaded image: {exc}'

                if not error:
                    if not extracted_text:
                        error = 'No readable text was found in the image.'
                    elif len(extracted_text) < 10:
                        error = 'The image contains too little text to analyze.'
                    else:
                        news_text = extracted_text

            if not error and news_text:
                if len(news_text) < 10:
                    error = 'Please enter at least 10 characters.'
                else:
                    prediction, confidence = predict_news(news_text)
            elif not error and not news_text:
                error = 'Enter news text or upload an image containing news text.'
        except Exception as exc:
            error = f'Prediction failed: {exc}'

    return render_template(
        'index.html', prediction=prediction, confidence=confidence,
        news_text=news_text, extracted_text=extracted_text, error=error
    )


@app.route('/dataset')
def dataset():
    csv_path = BASE_DIR / 'coda_text.csv'
    if not csv_path.exists():
        return render_template('dataset.html', rows=[], columns=[], total=0,
                               error='coda_text.csv was not found in the project folder.')
    try:
        df = pd.read_csv(csv_path)
        rows = df.head(25).fillna('').to_dict(orient='records')
        return render_template('dataset.html', rows=rows, columns=list(df.columns),
                               total=len(df), error=None)
    except Exception as exc:
        return render_template('dataset.html', rows=[], columns=[], total=0, error=str(exc))


if __name__ == '__main__':
    # Local-only development server. Do not use Flask debug mode on a public server.
    app.run(host='127.0.0.1', port=5000, debug=True)
