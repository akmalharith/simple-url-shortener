from flask import Flask, abort, render_template, request, redirect, Response
from tools.encoder import encode, decode
from tools.core import init_table, set_url, get_url
from urllib.parse import urlparse
import logging
logger = logging.getLogger(__name__)

TITLE = 'Simple URL shortener'
HOST = 'http://localhost:5000/'
PROTO = 'http://'

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Render home page, shows the input text for URL shortening
    """
    if request.method == 'POST':
        text = request.form['text']
        
        # Insert URL in the URL table
        try:
            if (urlparse(text).scheme == ''):
                textUrl = PROTO + text
            else:
                textUrl = text
            rowId = set_url(str.encode(textUrl))
        except Exception as e:
            logger.exception(str(e))
    
        # Encode it
        shortUrl = HOST + encode(rowId)

        return render_template('index.html', title=TITLE, show_results=True, short_url=shortUrl)

    return render_template('index.html', title=TITLE)

@app.route('/<short_url>')
def redirect_short_url(short_url):
    """
    Redirect paths based on the endpoint
    """
    # Decode a shortened URL
    decodedId = decode(str(short_url))
    url = HOST
    try:
        # Get from the URL table
        url = get_url(decodedId)
        return redirect(url)
    except Exception as e:
        error_message = str(e)
        logger.exception(error_message)

    # Throw a 404 for not found
    abort(Response(error_message, 404)) 

    # Or redirect back to HOST
    # return redirect(url)

if __name__ == '__main__':
    init_table()
    app.run(host='0.0.0.0')