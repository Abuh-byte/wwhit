from flask import Flask, redirect, request, session, render_template
import requests

app = Flask(__name__)
app.secret_key = "7522dd3c6af0f377f61b48e75772512c882a97290122d6e496c5f8bce4301530"

CLIENT_ID = "1469548050333831168"
CLIENT_SECRET = "hKapxq11_emvlipShcR_Rm4-zhJRLDgf"
REDIRECT_URI = "http://localhost:5000/callback"

DISCORD_AUTH_URL = "https://discord.com/api/oauth2/authorize"
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_API_URL = "https://discord.com/api/users/@me"


@app.route("/")
def index():
    user = session.get("user")
    return render_template("index.html", user=user)


@app.route("/login")
def login():
    return redirect(
        f"{DISCORD_AUTH_URL}"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify"
    )


@app.route("/callback")
def callback():
    code = request.args.get("code")

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "identify"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_res = requests.post(DISCORD_TOKEN_URL, data=data, headers=headers)
    token = token_res.json().get("access_token")

    user_res = requests.get(
        DISCORD_API_URL,
        headers={"Authorization": f"Bearer {token}"}
    )

    session["user"] = user_res.json()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)