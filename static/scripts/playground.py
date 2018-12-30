import requests

@app.route('/testing', methods = ['POST', 'GET'])
def searchbar():
    def fetchAddress():
        curLoc = request.form.get('curLoc')
        GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
        params = {
            'address': curLoc,
            'sensor': 'false'
        }
        # Do the request and get the response data
        req = requests.get(GOOGLE_MAPS_API_URL, params=params)
        res = req.json()

        # Use the first result
        result = res['results'][0]

        geodata = dict()
        geodata['lat'] = result['geometry']['location']['lat']
        geodata['lng'] = result['geometry']['location']['lng']
        geodata['address'] = result['formatted_address']


        print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))
