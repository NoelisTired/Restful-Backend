import threading, json, logging, MySQLdb, time, datetime, base64, random, string
from flask import request, jsonify, Flask, cli
from hashlib import sha256

debug = False

class FlaskApp(Flask):
    def __init__(self, name):
        super(FlaskApp, self).__init__(name)
        self.admin = Admin(FlaskApp)
        self.conf = json.load(open('./conf.json'))
        try: self.db = MySQLdb.connect(
                    host=self.conf['Database']['Host'],
                    port=self.conf['Database']['Port'],
                    user=self.conf['Database']['Login']['Username'],
                    passwd=self.conf['Database']['Login']['Password'],
                    db=self.conf['Database']['Login']['Database']
        )
        except: print("%s | [MySQL] Failed to connect to %s" % (time.strftime("%H:%M:%S"), f"{self.conf['Database']['Host']}:{self.conf['Database']['Port']}")); exit()
        self.cur = self.db.cursor()
        print("%s | [MySQL] - Connection Established to %s:%s" % (datetime.datetime.now().strftime("%H:%M:%S"), self.conf['Database']['Host'], self.conf['Database']['Port']))
        """
            ? Routes
            All routes are defined here and are called from the start() method
        """
        self.route('/', methods=['GET'])(self.home)
        self.route('/api/v1/register', methods=['GET'])(self.register)
        self.route('/api/v1/login', methods=['GET'])(self.login)
        self.route('/api/v1/getkey', methods=['GET'])(self.getKey)
        
        """
            ! Admin Routes
            All admin routes are defined here and are called from the start() method
        """
        self.route('/api/v1/admin', methods=['POST'])(self.admin.remove)
    def isAdmin(self, apikey: str) -> bool:
            #? Checks if the user is an admin
            #* Prepares the query and executes it, then commits the changes to the database
            query = "SELECT * FROM users WHERE APIKEY = %s AND ADMIN = 1"
            self.cur.execute(query, (apikey,))
            self.db.commit()
            return True if self.cur.rowcount else False
    def isDuplicate(self, username: str, discord=None) -> bool:
            #? Checks if the user is already in the database
            #* Prepares the query and executes it, then commits the changes to the database
            if discord:
                query = "SELECT * FROM users WHERE USERNAME = %s OR DISCORD = %s"
                self.cur.execute(query, (username, discord))
            else:
                query = "SELECT * FROM users WHERE USERNAME = %s"
                self.cur.execute(query, (username,))
            self.db.commit()
            return True if self.cur.rowcount else False
    def isAllowed(self, key: str, ua: str) -> bool:
        return True if key == sha256(base64.b64encode(datetime.datetime.now().strftime("%Y%m%d").encode())).hexdigest()[::-1][::-2]+"END+aHR0cHM6Ly95b3V0dS5iZS9pNjFHLXN1TFZkOD90PTYw" and ua == "NoelP X - Python Requests" else False
        
    """
        Below are all the @app.route() functions
    """
    def home(self) -> str:
        return jsonify("Flask app running on 127.0.0.1:5000")
    def getKey(self) -> str:
        #500 random words
        return jsonify({"Success": True, "Message": "Key generated", "Key": sha256(base64.b64encode(datetime.datetime.now().strftime("%Y%m%d").encode())).hexdigest()[::-1][::-2]+"END+aHR0cHM6Ly95b3V0dS5iZS9pNjFHLXN1TFZkOD90PTYw"})
    def register(self) -> dict:
        #? Hashes the username and password with sha256, then hexdigests it. I <3 my users privacy
        #* Prepares the query and executes it, then commits the changes to the database
        start = time.time()
        if not self.isAllowed(request.headers.get('X-Eric-Cartman'), request.headers.get('User-Agent')):
            return jsonify({"Success": False, "Message": "Access Denied"})
        username, password, apikey = request.headers.get('username'),\
                                sha256(request.headers.get('password').encode()).hexdigest(),\
                                    ''.join(random.sample(string.ascii_lowercase, 18))
        if self.isDuplicate(username, request.headers.get('discord') if request.headers.get('discord') else None):
            return jsonify({"Success": False, "Message": "User already exists"})
        if not request.headers.get('username') or not request.headers.get('password'):
            return jsonify({"Success": False, "Message": f"Missing argument '{'username' if not request.headers.get('username') else 'password'}'"})
        query = "INSERT INTO users (ID, USERNAME, PASSWORD, EMAIL, OAUTH, DISCORD, APIKEY, ADMIN) VALUES (NULL,%s,%s,'EMPTY','EMPTY',%s,%s,0)"
        self.cur.execute(query, (username, password, request.headers.get('discord') if request.headers.get('discord') else "EMPTY", apikey,))
        self.db.commit()
        [print("%s | [API] - Registered user %s" % (datetime.datetime.now().strftime("%H:%M:%S"), username)) if not request.headers.get('discord') else print("%s | [Discord] - Registered user %s with discord %s" % (datetime.datetime.now().strftime("%H:%M:%S"), username, request.headers.get('discord')))]
        return jsonify({"Success": True, "Message": f"Successfully logged in as {username}, Your account is not yet verified", "Time": time.time() - start})
    
    def login(self) -> dict:
        #? Hashes the username and password with sha256, then hexdigests it. I <3 my users privacy
        #* Prepares the query and executes it, then commits the changes to the database
        start = time.time()
        if not self.isAllowed(request.headers.get('X-Eric-Cartman'), request.headers.get('User-Agent')):
            return jsonify({"Success": False, "Message": "Access Denied"})
        username, password = request.headers.get('username'),\
                            sha256(request.headers.get('password').encode()).hexdigest()
        if not request.headers.get('username') or not request.headers.get('password'):
            return jsonify({"Success": False, "Message": f"Missing argument '{'username' if not request.headers.get('username') else 'password'}'"})
        #? Checks if the user is already in the database
        #* Prepares the query and executes it, then commits the changes to the database
        query = "SELECT * FROM users WHERE USERNAME = %s AND PASSWORD = %s"
        self.cur.execute(query, (username, password))
        if self.cur.rowcount:
            print("%s | [API] - %s has logged in successfully" % (datetime.datetime.now().strftime("%H:%M:%S"), username))
            return jsonify({"Success": True, "Message": f"Logged in as {username}", "Time": time.time() - start})
        else:
            return jsonify({"Success": False, "Message": "Invalid credentials", "Time": time.time() - start})
    """
        Start method
    """
    def start(self) -> threading.Thread:
        print("%s | [API] - Starting API server on %s:%s" % (datetime.datetime.now().strftime("%H:%M:%S"), self.conf['Api']['Host'], self.conf['Api']['Port']))
        cli.show_server_banner = lambda *args: None
        logging.getLogger('werkzeug').setLevel(logging.CRITICAL)
        return threading.Thread(target=lambda: self.run(host=self.conf['Api']['Host'], port=self.conf['Api']['Port'])) #? Starts the flask server on a separate thread
class Admin:
    #TODO Add admin functions
    def __init__(self, app: FlaskApp):
        self.isAdmin = app.isAdmin
        self.isAllowed = app.isAllowed
    def remove(self) -> str:
        if not request.headers.get('apikey') or not request.headers.get('username'):
            return jsonify({"Success": False, "Message": f"Missing argument '{'apikey' if not request.headers.get('apikey') else 'username'}'"})
        if not self.isAllowed(self, request.headers.get('X-Eric-Cartman'), request.headers.get('User-Agent')) or not self.isAdmin(FlaskApp(__name__), request.headers.get('apikey')):
            return jsonify({"Success": False, "Message": "Access Denied"})
        query = "DELETE FROM users WHERE USERNAME = %s"
        self.cur.execute(query, (request.headers.get('username'),))
        self.db.commit()
        print("%s | [ADMIN] - Removed user %s" % (datetime.datetime.now().strftime("%H:%M:%S"), request.headers.get('username')))
        return jsonify({"Success": True, "Message": f"Successfully Removed {request.headers.get('username')}"})
    def add(self) -> str:
        if not request.headers.get('apikey') or not request.headers.get('username'):
            return jsonify({"Success": False, "Message": f"Missing argument '{'apikey' if not request.headers.get('apikey') else 'username'}'"})
        if not self.isAllowed(self, request.headers.get('X-Eric-Cartman'), request.headers.get('User-Agent')) or not self.isAdmin(FlaskApp(__name__), request.headers.get('apikey')):
            return jsonify({"Success": False, "Message": "Access Denied"})
        query = "INSERT INTO users (ID, USERNAME, PASSWORD, EMAIL, OAUTH, DISCORD, APIKEY, ADMIN) VALUES (NULL,%s,%s,'EMPTY','EMPTY','EMPTY',%s,0)"
        self.cur.execute(query, (request.headers.get('username'), request.headers.get('password'), ''.join(random.sample(string.ascii_lowercase, 18)),))
        self.db.commit()
        

if __name__ != '__main__' and debug != True:
    app = FlaskApp(__name__).start()
    app.daemon = True
    app.start()