import flask
import os
import logging
from fitbit import Fitbit
from urllib.parse import urljoin
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


app = flask.Flask(__name__)
app.secret_key = 'too long secret'

redirect_path = '/callback'

"""
DEBUG:requests_oauthlib.oauth2_session:Response headers were {
'Date': 'Wed, 08 May 2019 09:17:41 GMT', 'Content-Type': 'application/json;charset=utf-8', 'Transfer-Encoding': 'chunked',
 'Connection': 'keep-alive', 'Vary': 'Origin,Accept-Encoding', 'Cache-control': 'no-cache, private', 
 'WWW-Authenticate': 'Basic realm="api.fitbit.com"', 'Content-Language': 'ja-JP', 'Content-Encoding': 'gzip',
'X-Frame-Options': 'SAMEORIGIN, SAMEORIGIN', 'Expect-CT': 'max-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"', 
'Server': 'cloudflare', 'CF-RAY': '4d3a578bec34a5c4-NRT'} 
and content {"errors":[{"errorType":"invalid_client",
"message":"Invalid authorization header format. The client id was not provided in proper format inside Authorization Header. 
Received authorization header = Basic MjJEUFFYOg==,  received client encoded id = null. 
Visit https://dev.fitbit.com/docs/oauth2 for more information on the Fitbit Web API authorization process."}],
"success":false}.
"""


@app.route('/')
def hello():
    return 'hello'


@app.route('/login')
def login():
    fitbit = Fitbit(
        client_id=os.environ['FITBIT_CLIENT_ID'],
        client_secret=os.environ['FITBIT_CLIENT_SECRET'],
        redirect_uri=urljoin(flask.request.host_url, redirect_path)
    )
    print(urljoin(flask.request.host_url, redirect_path))
    url, state = fitbit.client.authorize_token_url(scope=None)
    flask.session['login_state'] = state
    print(f'redirect url is {url}')
    return flask.redirect(url)

@app.route('/callback')
def callback():
    print(urljoin(flask.request.host_url, redirect_path))
    fitbit = Fitbit(
        client_id=os.environ['FITBIT_CLIENT_ID'],
        client_secret=os.environ['FITBIT_CLIENT_SECRET'],
        redirect_uri=urljoin(flask.request.host_url, redirect_path),
        state=flask.session['login_state']
    )
    print(flask.request.args.get('code'))
    fitbit.client.fetch_access_token(code=flask.request.args.get('code'))

    return 'ok'


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
