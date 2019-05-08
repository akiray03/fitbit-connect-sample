import flask
import os
from fitbit import Fitbit
from urllib.parse import urljoin


app = flask.Flask(__name__)

redirect_path = '/callback'


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
    url, _ = fitbit.client.authorize_token_url(scope=None)
    print(f'redirect url is {url}')
    return flask.redirect(url)

@app.route('/callback')
def callback():
    print(urljoin(flask.request.host_url, redirect_path))
    fitbit = Fitbit(
        client_id=os.environ['FITBIT_CLIENT_ID'],
        client_secret=os.environ['FITBIT_CLIENT_SECRET'],
        redirect_uri=urljoin(flask.request.host_url, redirect_path)
    )
    print(flask.request.args.get('code'))
    fitbit.client.fetch_access_token(code=flask.request.args.get('code'))

    return 'ok'


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
