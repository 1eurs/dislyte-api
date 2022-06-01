import esper as esper
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pprint import pprint
from flask import Flask, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URLL", "sqlite:///characters.db")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    rate = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(250), nullable=False)
    stars = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)


# SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# SERVICE_ACCOUNT_FILE = 'dislyte-c2e741e0964b.json'
# creds = None
# creds = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#
# SAMPLE_SPREADSHEET_ID = '13ISaHcyxIrlx0uCmfGKjwvqZlN8wzQFv9kQAX8vpykw'
#
# service = build('sheets', 'v4', credentials=creds)
#
# sheet = service.spreadsheets()
# result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                             range="TierList!C3:E79").execute()
# result2 = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
#                              range="TierList!N3:N79").execute()
# values = result.get('values', [])
# valuess = result2.get('values', [])
#
# for i in range(len(values)):
#     values[i].append(valuess[i][0])
#
# characters = []
# for value in values:
#     character = {
#         "name": value[0],
#         "stars": value[1],
#         "role": value[2],
#         "rate": value[3],
#     }
#     characters.append(character)

# for char in characters:
#     i = str(characters.index(char))
#     new_char = Characters(
#         name=char["name"],
#         stars=char["stars"],
#         role=char["role"],
#         rate=char["rate"],
#         img_url="/images/esper" + i
#     )
# db.session.add(new_char)
# db.session.commit()


@app.route("/all")
def get_all_char():
    chars = db.session.query(Characters).all()
    chars_list = []
    for chars_value in chars:
        characters_ = {
            "id": chars_value.id,
            "name": chars_value.name,
            "role": chars_value.role,
            "img_url": chars_value.img_url,
            "stars": chars_value.stars,
            "rate": chars_value.rate,
        }
        chars_list.append(characters_)
    return jsonify(chars_list)


@app.route('/images/<esper_>')
def get_image(esper_):
    return send_from_directory(directory="static/images", path=f"{esper_}.png")


if __name__ == "__main__":
    app.run()

# folder = "images"
# for count, filename in enumerate(os.listdir(folder)):
#     dst = f"esper{str(count)}.png"
#     src = f"{folder}/{filename}"  # foldername/filename, if .py file is outside folder
#     dst = f"{folder}/{dst}"
#
#     # rename() function will
#     # rename all the files
#     os.rename(src, dst)
