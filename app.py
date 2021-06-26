import sys
import os
import glob
import atexit
import hashlib
import json
import shutil
from os import getcwd, path, makedirs
from shutil import rmtree, make_archive as archive, copytree
from pathlib import Path
from flask import Flask, redirect, \
    render_template, request, url_for, jsonify, \
    send_file
from apscheduler.schedulers.background import BackgroundScheduler
from pytube import YouTube, Playlist
from datetime import date, datetime
from uuid import uuid4 as UUID

storage_dir = os.environ.get('STORAGE_DIR', Path(getcwd()) / 'storage')
PORT = os.environ.get('PORT', 8080)

if not Path(storage_dir).is_dir():
    makedirs(storage_dir)

app = Flask(__name__)
scheduler = BackgroundScheduler(daemon=True)

def showtime():
    # datetime.datetime.isoformat(datetime.datetime.fromisoformat(l))
    print(datetime.now().isoformat())
    dirs = filter(lambda p: Path(p).is_dir(), glob.glob(path.join(storage_dir, '*')))
    for dir in dirs:
        if path.split(dir)[-1] != 'playlists':
            try:
                with open(path.join(dir, 'info.json'), 'r', encoding='utf-8') as f:
                    info = json.load(f)
                    dt = (datetime.now() - datetime.fromisoformat(info['time'])).total_seconds() / 60
                if dt >= 30:
                    print(f'Deleting {info["name"]}')
                    rmtree(dir)
            except:
                ...
    pdirs = filter(lambda p: Path(p).is_dir(), glob.glob(path.join(storage_dir, 'playlists', '*')))
    for dir in pdirs:
        try:
            with open(path.join(dir, 'info.json'), 'r', encoding='utf-8') as f:
                info = json.load(f)
                dt = (datetime.now() - datetime.fromisoformat(info['time'])).total_seconds() / 60
            if dt >= 30:
                print(f'Deleting {info["name"]}')
                rmtree(dir)
        except:
            ...

def md5(s: str):
    return hashlib.md5(s.encode()).hexdigest()

def er(msg: str, status: int = 400):
    return jsonify({
        'msg': msg
    }), status

if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
    scheduler.add_job(id='showtime', func=showtime, trigger='interval', seconds=600)
    scheduler.start()
    atexit.register(scheduler.shutdown)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/api', methods=['POST', 'GET'])
def api():
    if request.method == 'POST':
        video = request.json.get('url')
        qua = request.json.get('quality')
        print(video, qua)
        downloaded = None
        try:
            video_local_uid = md5(video)
            p = path.join(storage_dir, video_local_uid)
            if not Path(p).is_dir():
                o = YouTube(video)
                fname = o.streams.first().default_filename
                if qua == '2':
                    o.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(p)
                else:
                    o.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').asc().first().download(p)
                info = {
                    'name': fname,
                    'url': video,
                    'time': datetime.now().isoformat()
                }
                with open(path.join(p, 'info.json'), 'w', encoding='utf-8') as f:
                    json.dump(info, f)
                downloaded = info
            else:
                with open(path.join(p, 'info.json'), 'r', encoding='utf-8') as f:
                    info = json.load(f)
                info['time'] = datetime.now().isoformat()
                with open(path.join(p, 'info.json'), 'w', encoding='utf-8') as f:
                    json.dump(info, f)
                downloaded = info
            return jsonify({
                'name': downloaded['name'],
                'url': downloaded['url'],
                'id': video_local_uid
            })
        except Exception as e:
            print(f'Error: {e.args}', file=sys.stderr)
            return er('Error!'), 400
    else:
        url = request.args.get('url')
        try:
            playlist = Playlist(url)
            videos = tuple(playlist.video_urls)
            def video_details(v):
                video_local_uid = md5(v)
                p = path.join(storage_dir, video_local_uid)
                if not Path(p).is_dir():
                    try:
                        o = YouTube(v)
                        fname = o.streams.first().default_filename
                        return {
                            'name': '.'.join(fname.split('.')[:-1]),
                            'url': v,
                            'id': video_local_uid
                        }
                    except:
                        return None
                else:
                    try:
                        with open(path.join(p, 'info.json'), 'r', encoding='utf-8') as f:
                            info = json.load(f)
                        return {
                            'name': '.'.join(info['name'].split('.')[:-1]),
                            'url': info['url'],
                            'id': video_local_uid
                        }
                    except:
                        return None
            
            videos = tuple(map(video_details, videos))
            return jsonify({
                'videos': videos
            })
        except Exception as e:
            print(f'Error: {e.args}', file=sys.stderr)
            return er('Invalid playlist URL!')

@app.route('/download-playlist')
def download_playlist():
    purl = request.args.get('purl')
    if purl is None:
        return er('No URL given.')
    # try:
    playlist = Playlist(purl)
    videos = tuple(playlist.video_urls)
    def video_details(v):
        video_local_uid = md5(v)
        p = path.join(storage_dir, video_local_uid)
        if not Path(p).is_dir():
            try:
                o = YouTube(v)
                fname = o.streams.first().default_filename
                return {
                    'name': '.'.join(fname.split('.')[:-1]),
                    'url': v,
                    'id': video_local_uid
                }
            except:
                return None
        else:
            try:
                with open(path.join(p, 'info.json'), 'r', encoding='utf-8') as f:
                    info = json.load(f)
                return {
                    'name': '.'.join(info['name'].split('.')[:-1]),
                    'url': info['url'],
                    'id': video_local_uid
                }
            except:
                return None
    
    videos = tuple(map(video_details, videos))
    videos = tuple(filter(lambda x: x is not None, videos))
    videos = tuple(map(lambda x: x['id'], videos))

    pl_id = md5(purl)
    pl = path.join(storage_dir, 'playlists', pl_id)
    if (Path(pl) / 'videos').is_dir():
        rmtree(Path(pl) / 'videos')
    makedirs(path.join(pl, 'videos'), exist_ok=True)
    for video_id in videos:
        vp = path.join(storage_dir, video_id)
        with open(path.join(vp, 'info.json'), 'r', encoding='utf-8') as f:
            info = json.load(f)
        fp = path.join(vp, info['name'])
        shutil.copy(fp, path.join(pl, 'videos'))
    if Path(pl).is_dir():
        fn = archive(path.join(pl, f'videos-{UUID()}'), 'zip', path.join(pl, 'videos'))
        info = {
            'name': fn,
            'url': purl,
            'id': pl_id,
            'time': datetime.now().isoformat()
        }
        with open(path.join(pl, 'info.json'), 'w', encoding='utf-8') as f:
            json.dump(info, f)
        return send_file(path.join(storage_dir, 'playlists', pl_id, info['name']))
    else:
        with open(path.join(pl, 'info.json'), 'r', encoding='utf-8') as f:
            info = json.load(f)
        return send_file(path.join(storage_dir, 'playlists', pl_id, info['name']))
    # except Exception as e:
    #     print(f'Error: {e.args}', file=sys.stderr)
    #     return er('Invalid playlist URL!')

@app.route('/download/<local_id>')
def download(local_id):
    p = Path(storage_dir) / str(local_id)
    if not p.is_dir():
        return er('File not found. Please try again.')
    try:
        with open(path.join(p, 'info.json'), 'r', encoding='utf-8') as f:
            info = json.load(f)
        return send_file(p / info['name'])
    except:
        return er('Failed to retrieve file.', 500)

if __name__ == "__main__":
    app.run(port=PORT, debug=True)