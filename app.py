

from flask import Flask, render_template, send_from_directory, request  # Add request here
import os
import re
from datetime import datetime


app = Flask(__name__)

#BASE_DIR = "/Users/grantvurpillat/Desktop/BB_RTT/"
BASE_DIR = "/Volumes/GV64GB/BB_RTT/"


@app.route('/')
def index():
    folder_names = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f))]
    
    # Sort folder names based on the date.
    # If the folder name can't be parsed into a date, put it at the end.
    folder_names = sorted(folder_names, key=lambda x: datetime.strptime(x, '%Y-%m-%d') if re.match(r'\d{4}-\d{2}-\d{2}', x) else datetime.max)
    
    return render_template('index.html', folder_names=folder_names)

@app.route('/folder/<folder_name>')
def show_videos(folder_name):
    video_dir = os.path.join(BASE_DIR, folder_name)
    #video_names = sorted(os.listdir(video_dir), key=lambda x: int(''.join(filter(str.isdigit, x))), reverse=True)
    #video_names = sorted(os.listdir(video_dir), key=lambda x: int(''.join(filter(str.isdigit, x))) if filter(str.isdigit, x) else 0, reverse=True)
    video_names = [f for f in os.listdir(video_dir) if any(char.isdigit() for char in f)]
    #video_names = sorted(video_names, key=lambda x: int(''.join(filter(str.isdigit, x))))
    video_names = sorted(video_names, key=lambda x: int(re.search(r'\d+', x).group(0)) if re.search(r'\d+', x) else 0)
    return render_template('videos.html', video_names=video_names, folder_name=folder_name)



@app.route('/video/<folder_name>/<video_name>')
def video(folder_name, video_name):
    video_dir = os.path.join(BASE_DIR, folder_name)
    return send_from_directory(video_dir, video_name)


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = ""
    search_results = []

    if request.method == 'POST':
        query = request.form.get('query')
        for folder_name in os.listdir(BASE_DIR):
            folder_path = os.path.join(BASE_DIR, folder_name)
            if os.path.isdir(folder_path):  # Check if it's a directory
                video_dir = folder_path
                for video_name in os.listdir(video_dir):
                    if query.lower() in video_name.lower():
                        search_results.append((folder_name, video_name))

    return render_template('search.html', video_names=search_results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
