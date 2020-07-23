import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
import app_config_b2c
import msal

from . import web


@web.route("/")
def index():
    if not session.get("user"):
        # session["state"] = str(uuid.uuid4())
        # auth_url = _build_auth_url(scopes=app_config_b2c.SCOPE,
        #                        state=session["state"])
        # return redirect(auth_url)
        return redirect(url_for("web.login"))
    return render_template('index.html',
                           user=session["user"],
                           version=msal.__version__)


@web.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    auth_url = _build_auth_url(scopes=app_config_b2c.SCOPE,
                               state=session["state"])
    return render_template("login.html",
                           auth_url=auth_url,
                           version=msal.__version__)


@web.route(app_config_b2c.REDIRECT_PATH
           )  # Its absolute URL must match your app's redirect_uri set in AAD
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for("web.index"))  # No-OP. Goes back to Index page
    if "error" in request.args:  # Authentication/Authorization failure
        return render_template("auth_error.html", result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(
            cache=cache).acquire_token_by_authorization_code(
                request.args['code'],
                scopes=app_config_b2c.
                SCOPE,  # Misspelled scope would cause an HTTP 400 error here
                redirect_uri=url_for("web.authorized", _external=True))
        if "error" in result:
            return render_template("auth_error.html", result=result)
        session["user"] = result.get("id_token_claims")
        _save_cache(cache)
    return redirect(url_for("web.index"))


@web.route("/logout")
def logout():
    session.clear()  # Wipe out user and its token cache from session
    return redirect(  # Also logout from your tenant's web session
        app_config_b2c.AUTHORITY + "/oauth2/v2.0/logout" +
        "?post_logout_redirect_uri=" + url_for("web.index", _external=True))


@web.route("/graphcall")
def graphcall():
    token = _get_token_from_cache(app_config_b2c.SCOPE)
    if not token:
        return redirect(url_for("web.login"))
    graph_data = requests.get(  # Use token to call downstream service
        app_config_b2c.ENDPOINT,
        headers={
            'Authorization': 'Bearer ' + token['access_token']
        },
    ).json()
    return render_template('display.html', result=graph_data)


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache


def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config_b2c.CLIENT_ID,
        authority=authority or app_config_b2c.AUTHORITY,
        client_credential=app_config_b2c.CLIENT_SECRET,
        token_cache=cache)


def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("web.authorized", _external=True))


def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result


# app.jinja_env.globals.update(
#     _build_auth_url=_build_auth_url)  # Used in template

# @main.route('/')
# def index():
#     return render_template('index.html')

# @main.route('/home')
# def home():
#     return render_template('home.html')

# @main.route('/health', methods=['GET'])
# def health():
#     return jsonify({'ApplicationName': 'WeldDefectDetectionAI'})

# @main.route('/predict', methods=['POST'])
# def post():
#     r = requests.post('http://localhost/api/ai/detect',
#                     json=request.get_json())
#     return r.json(), r.status_code