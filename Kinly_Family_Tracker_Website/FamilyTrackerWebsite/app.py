from flask import Flask, render_template, request, jsonify
import sqlite3, os, secrets, time

app = Flask(__name__)
DB = os.environ.get('FAMILY_TRACKER_DB', 'family_tracker.db')

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.execute('''CREATE TABLE IF NOT EXISTS members (id TEXT PRIMARY KEY, name TEXT NOT NULL, token TEXT NOT NULL, lat REAL, lon REAL, accuracy REAL, updated REAL, sharing INTEGER NOT NULL DEFAULT 1)''')
    con.commit()
    return con

def member_from_request(con):
    token = request.headers.get('Authorization', '').removeprefix('Bearer ').strip()
    if not token:
        return None
    return con.execute('SELECT * FROM members WHERE token=?', (token,)).fetchone()

@app.get('/')
def home():
    return render_template('index.html')

@app.post('/api/register')
def register():
    data = request.get_json(silent=True) or {}
    name = str(data.get('name', '')).strip()[:50]
    if not name:
        return jsonify(error='Please enter a name.'), 400
    con = db(); mid = secrets.token_urlsafe(10); token = secrets.token_urlsafe(32)
    con.execute('INSERT INTO members(id,name,token,updated,sharing) VALUES(?,?,?,?,1)', (mid,name,token,time.time()))
    con.commit(); con.close()
    return jsonify(id=mid, name=name, token=token)

@app.get('/api/members')
def members():
    con=db(); rows=con.execute('SELECT id,name,lat,lon,accuracy,updated,sharing FROM members ORDER BY name COLLATE NOCASE').fetchall(); con.close()
    return jsonify([dict(r) for r in rows])

@app.post('/api/location')
def location():
    con=db(); me=member_from_request(con)
    if not me: con.close(); return jsonify(error='Register this device first.'), 401
    data=request.get_json(silent=True) or {}
    try: lat=float(data['lat']); lon=float(data['lon'])
    except (KeyError,TypeError,ValueError): con.close(); return jsonify(error='Invalid coordinates.'),400
    if not (-90 <= lat <= 90 and -180 <= lon <= 180): con.close(); return jsonify(error='Invalid coordinates.'),400
    con.execute('UPDATE members SET lat=?,lon=?,accuracy=?,updated=?,sharing=1 WHERE id=?', (lat,lon,float(data.get('accuracy') or 0),time.time(),me['id']))
    con.commit(); con.close(); return jsonify(ok=True)

@app.post('/api/sharing')
def sharing():
    con=db(); me=member_from_request(con)
    if not me: con.close(); return jsonify(error='Register this device first.'),401
    enabled=1 if (request.get_json(silent=True) or {}).get('enabled') else 0
    con.execute('UPDATE members SET sharing=?,updated=? WHERE id=?',(enabled,time.time(),me['id']))
    con.commit(); con.close(); return jsonify(ok=True)

@app.post('/api/remove')
def remove():
    con=db(); me=member_from_request(con)
    if not me: con.close(); return jsonify(error='Register this device first.'),401
    con.execute('DELETE FROM members WHERE id=?',(me['id'],)); con.commit(); con.close(); return jsonify(ok=True)

if __name__ == '__main__':
    db().close()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
