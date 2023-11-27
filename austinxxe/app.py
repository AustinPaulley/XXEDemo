from flask import Flask, request, render_template_string
from lxml import etree
from defusedxml.ElementTree import fromstring

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <html>
            <head>
                <title>XXE Demo: Vulnerable and Secure</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 2em; }
                    h2, p { color: #333; }
                    form { margin-top: 1em; }
                    .result { border: 1px solid #ccc; padding: 10px; margin-top: 20px; }
                </style>
            </head>
            <body>
                <h2>XML File Upload</h2>
                <p>Choose an upload method:</p>
                <form action="/vulnerable_upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <input type="submit" value="Vulnerable Upload">
                </form>
                <form action="/secure_upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <input type="submit" value="Secure Upload">
                </form>
            </body>
        </html>
    '''

@app.route('/vulnerable_upload', methods=['POST'])
def vulnerable_upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        try:
            file_content = file.stream.read()  # Read as bytes
            parser = etree.XMLParser(load_dtd=True, no_network=False)
            doc = etree.fromstring(file_content, parser=parser)
            extracted_data = etree.tostring(doc, pretty_print=True, encoding='UTF-8').decode('UTF-8')
            return render_template_string('<p>Parsed Content:</p><div class="result">' + extracted_data + '</div>')
        except Exception as e:
            return f"<p>Error: {e}</p>"
    return 'File processing failed.'

@app.route('/secure_upload', methods=['POST'])
def secure_upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        try:
            file_content = file.stream.read().decode('UTF-8')
            tree = fromstring(file_content)
            extracted_data = etree.tostring(tree, pretty_print=True, encoding='UTF-8').decode('UTF-8')
            return render_template_string('<p>Parsed Content:</p><div class="result">' + extracted_data + '</div>')
        except Exception as e:
            return f"<p>Error: {e}</p>"
    return 'File processing failed.'

if __name__ == '__main__':
    app.run(debug=True)

