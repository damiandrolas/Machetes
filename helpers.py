import os
# import requests
import urllib.parse
import datetime

from flask import redirect, render_template, request, session
from functools import wraps


import re   
  
# "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
  
def check(email):   
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
    return re.search(regex,email)


def datetime_format(value, format="%A %d-%m-%y"):
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<", value)
    year = int(value[:4])
    day = int(value[5:7])
    mes = int(value[8:10])
    fecha = datetime.datetime(year, day, mes)
    fecha = fecha.strftime(format)
    d = {"Monday":"Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday":"Viernes", "Saturday": "Sábado", "Sunday":"Domingo"}
    for key in d:
        if key in fecha:
            fecha = fecha.replace(key,d[key])
    
    return fecha


def apology(message, code=400):
    """Render message as an apology to user."""
    # def escape(s):
    #     """
    #     Escape special characters.

    #     https://github.com/jacebrowning/memegen#special-characters
    #     """
    #     for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
    #                      ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
    #         s = s.replace(old, new)
    #     return s
    return render_template("apology.html", message=message)


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


    


# def lookup(symbol):
#     """Look up quote for symbol."""

#     # Contact API
#     try:
#         api_key = os.environ.get("API_KEY")
#         url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
#         response = requests.get(url)
#         response.raise_for_status()
#     except requests.RequestException:
#         return None

    # Parse response
#     try:
#         quote = response.json()
#         return {
#             "name": quote["companyName"],
#             "price": float(quote["latestPrice"]),
#             "symbol": quote["symbol"]
#         }
#     except (KeyError, TypeError, ValueError):
#         return None


# def usd(value):
#     """Format value as USD."""
#     return f"${value:,.2f}"
