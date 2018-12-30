from flask import Flask, url_for, render_template, request, make_response
import pymysql
import json

app = Flask(__name__)

@app.route('/')
def home(first_name = ""):
    if request.cookies.get('first_name') != None:
        return render_template('index.html', first_name = request.cookies.get('first_name'))
    return render_template('index.html')

@app.route('/search')
def search(first_name = ""):
    if request.cookies.get('first_name') != None:
        return render_template('search.html', first_name = request.cookies.get('first_name'))
    return render_template('search.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signedup')
def signedup():
    return render_template("singedup.html")

@app.route('/plop')
def add():
    return render_template("add.html")

class Database:
    def __init__(self, b = False):
        host = "45.33.72.127"
        user = "plopper"
        password = "password"
        db = "PlopperPlops"

        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def run_script(s):
        self.cur.execute(s)
        result = self.cur.fetchall()
        self.con.commit()
        return result

    def login(self, u, p):
        self.cur.execute("SELECT * FROM userinfo WHERE email = '%s' AND passwd = '%s';" % (u,p,))
        result = self.cur.fetchall()
        return result

    def create_user(self, f, l, e, p):
        res = self.cur.execute("INSERT INTO userinfo (first_name, last_name, email, passwd) VALUES ('%s', '%s', '%s', '%s');" % (f, l, e, p))
        self.con.commit()
        print(res)
        return 0

@app.route('/login', methods = ['POST', 'GET'])
def login_form(first_name = ""):
    def db_query(s, b=False):
        db = Database(b)
        emps = db.run_script(s)
        return emps

    def db_login(u,p):
        db = Database()
        emps = db.login(u, p)
        return emps

    def db_create_user(f,l,e,p):
        db = Database()
        emps = db.create_user(f,l,e,p)
        return 0

    val = request.form.get('buttony')
    if request.method == 'POST':
        if val == "login":
            email = request.form.get('emaily')
            passwd = request.form.get('passwordy')
            res = db_login(email, passwd)
            if(len(res) == 0):
                return render_template("login.html")
            fresp = make_response(render_template("index.html", first_name = res[0]['first_name']))
            fresp.set_cookie("first_name", res[0]['first_name'])
            fresp.set_cookie("last_name", res[0]['last_name'])
            fresp.set_cookie("email", res[0]['email'])
            return fresp

        elif val == "signup":
            fname = request.form.get('firsty')
            lname = request.form.get('lasty')
            email = request.form.get('emaily2')
            passwd = request.form.get('passwordy2')
            db_create_user(fname, lname, email, passwd)
            return render_template("singedup.html")


@app.route('/', methods = ['POST'])
@app.route('/login', methods = ['POST'])
def logout(first_name = ""):
    if request.method == 'POST':
        fresp = make_response(render_template("index.html"))
        fresp.delete_cookie('first_name', path='/')
        fresp.delete_cookie('last_name', path='/')
        fresp.delete_cookie('email', path='/')
        return fresp

@app.route('/', methods = ['GET'])
@app.route('/login', methods = ['GET'])
def searchbar(withinRange = ""):
    print ("curloc")
    if request.method == 'GET':
        curLoc = request.form.get('curLoc')
            # curLoc = "Ann Arbor"
        GOOGLE_MAPS = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + curLoc + '&key=AIzaSyDif60flZknFREzxQ30gPgBNgnKculXuVc'
            # Do the request and get the response data
        req = requests.get(GOOGLE_MAPS)
        parsed_json = json.loads(req.text)

        curLat = parsed_json['results'][0]['geometry']['location']['lat']
        curLon = parsed_json['results'][0]['geometry']['location']['lng']

        db = Database(b)
        s = 'SELECT lat FROM toilets WHERE (lat - %s) < 0.002 AND (lat - %s) > -0.002 AND (long - %s) < 0.002 AND (long - %s) > -0.002;' % (curLat, curLat, curLon, curLon)
        withinRange = db.run_script(s)
        return render_template("search.html", withinRange = withinRange)

if __name__ == '__main__':
    app.run(debug=True)
