from flask import Flask, render_template, request
from os import getenv
from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(getenv('MONGODB_URI'))
    # 'mongodb+srv://cyber:MainADS2000@microblog.wl4ox.mongodb.net/'
    app.db = client.microblog

    @app.route('/', methods=['GET', 'POST'])
    def home():

        if request.method == 'POST':
            entry_content = request.form.get('content')
            formatted_date = datetime.today().strftime('%Y-%m-%d')
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.strptime(entry['date'], '%Y-%m-%d').strftime('%b %d')
            )

            for entry in app.db.entries.find({})
        ]
        return render_template('home.html', entries=entries_with_date)
    
    return app