import os
from flask import Flask, request, jsonify, render_template
from firebase_admin import credentials, firestore, initialize_app
from flask_googlemaps import GoogleMaps, Map


# Initialize Flask App
app = Flask(__name__, template_folder='./templates')
# Initialize Firestore DB
cred = credentials.Certificate("trackjet-1575190666888-firebase-adminsdk-1ch27-3eb99862f3.json")
default_app = initialize_app(cred)
db = firestore.client()
warehouse_ref = db.collection('warehouses')
users_ref = db.collection('users')


GoogleMaps(app, key="AIzaSyCCRbQEwkGNwLu5UczmtxKs1vbBJvY-Eos")



@app.route("/map")
def mapview():
    try:
        lat, long, name, img = [], [], [], []
        for i in warehouse_ref.stream():
            warehouse = i.to_dict()
            lat.append(float(warehouse["lat"]))
            long.append(float(warehouse["long"]))
            name.append(warehouse["name"])
            img.append(warehouse["img"])
        markers = []
        for x, y, z, img in zip(lat, long, name, img):
            d = {}
            d["icon"] = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
            d['lat'] = x
            d['lng'] = y
            z = z.split(",")
            d['infobox'] = "<b>{}</b><img src='{}' />".format(z[0], img)
            markers.append(d)

        sndmap = Map(
            identifier="sndmap",
            lat=lat[0],
            lng=long[0],
            markers=markers,
            fit_markers_to_bounds=True
        )
        return render_template('example.html', sndmap=sndmap)
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route("/user_map")
def user_mapview():
    try:
        lat, long, name, img = [], [], [], []
        for i in users_ref.stream():
            user = i.to_dict()
            lat.append(float(user["lat"]))
            long.append(float(user["long"]))
            name.append(user["name"])
        markers = []
        for x, y, z in zip(lat, long, name):
            d = {}
            d["icon"] = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
            d['lat'] = x
            d['lng'] = y
            d['infobox'] = "<b>{}</b> />".format(z)
            markers.append(d)

        sndmap = Map(
            identifier="sndmap",
            lat=lat[0],
            lng=long[0],
            markers=markers,
            fit_markers_to_bounds=True
        )
        return render_template('example.html', sndmap=sndmap)
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route("/index")
def home():
    return render_template("home.html")

@app.route('/locate')
def locate():
    return render_template('marker_locator.html')


@app.route('/add', methods=['POST'])
def create():
    """
        create() : Add document to Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        req = request.form
        print(req)
        hero = warehouse_ref.document()
        hero.set(req)
        return render_template("location_added.html")

    except Exception as e: 
        return f"An Error Occured: {e}"


@app.route('/list', methods=['GET'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON
        warehouse : Return document that matches query ID
        all_warehouses : Return all documents
    """
    try:
        warehouse_id = request.args.get('id')
        if warehouse_id:
            warehouse = warehouse_ref.document(warehouse_id).get()
            return jsonify(warehouse.to_dict()), 200
        else:
            all_warehouses = [doc.to_dict() for doc in warehouse_ref.stream()]
            return jsonify(all_warehouses), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/assign')
def assign():
    return render_template("assign.html")

@app.route('/assignmap', methods=['GET'])
def assignmap():
    user_id = request.args.get('user')
    warehouse_id = request.args.get('warehouse')
    loc = {}
    loc['lat_u'], loc['long_u'], loc['lat_w'], loc['long_w'] = 0, 0, 0, 0
    for doc in users_ref.stream():
        user = doc.to_dict()
        if user['name'] == user_id:
            loc['lat_u'], loc['long_u'] = user['lat'], user['long']
            break;
    else:
        return('notfound.html')

    for doc in warehouse_ref.stream():
        warehouse = doc.to_dict()
        print(warehouse['name'], warehouse_id, warehouse['name'] == warehouse_id)
        if warehouse['name'] == warehouse_id:
            loc['lat_w'], loc['long_w'] = warehouse['lat'], warehouse['long']
            break;
    else:
        return('notfound.html')

    return render_template("assignmap.html", loc=loc)

    
    

@app.route('/update', methods=['POST', 'PUT'])
def update():
    """
        update() : Update document in Firestore collection with request body
        Ensure you pass a custom ID as part of json body in post request
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        warehouse_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)
