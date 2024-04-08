from flask import Flask, Response, request, render_template, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_url_path='/', static_folder='static')
app.debug = True
CORS(app)

def list_videos():
    with open('../database/database.json', 'r') as f:
        return json.load(f)
    
def find_video_by_id(uuid):
    videos = list_videos()
    for video in videos:
        if video['id'] == uuid:
            return video
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videos')
def videos():
    list = []
    for video in list_videos():
        list.append({
            'id': video['id'],
            'title': video['title'],
            'watch_url': f'/watch?i={video["id"]}',
            'thumbnail_url': f'/thumbnails/{video["id"]}'
        })
    return list

@app.route('/watch')
def watch():
    id = request.args.get('i')
    video = find_video_by_id(id)
    return render_template('watch.html', id=video['id'], title=video['title'], url=f'/stream/{video["id"]}')

@app.route('/thumbnails/<string:id>')
def thumbnails(id):
    video = find_video_by_id(id)
    thumbnail_path = f"{video['id']}.jpg"
    return send_from_directory('../database/thumbnails', thumbnail_path)

@app.route('/stream/<string:id>')
def video(id):
    video = find_video_by_id(id)
    
    def generate():
        path_to_videos = '../database/videos'
        video_file = video['id'] + '.mp4'
        filename = f'{path_to_videos}/{video_file}'
        with open(filename, 'rb') as video_file:
            chunk_size = 1024 * 1024  # 1MB chunks
            chunk = video_file.read(chunk_size)
            while chunk:
                yield chunk
                chunk = video_file.read(chunk_size)
    return Response(generate(), mimetype='video/mp4')



if __name__ == '__main__':
    app.run()