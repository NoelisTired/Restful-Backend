import requests, getpass

"""
Example of how to use my API

NoelP#0561

"""

def getKey() -> str:
    try:
        r = requests.get("http://127.0.0.1:5000/api/v1/getkey")
        return r.json()["Key"]
    except requests.exceptions.ConnectionError:
        print("Server is down...")
    except:
        print("Unknown error...")
        input(); exit()
def login(username, password) -> bool:
    r = requests.get("http://127.0.0.1:5000/api/v1/login", headers={"User-Agent": "NoelP X - Python Requests","X-Eric-Cartman": getKey(),"username": username,"password": password})
    if r.status_code != 200: print("Server is down..."); input(); exit(0)
    print(r.json())
    return r.json()["Success"]

def register(username, password) -> bool:
    try: r = requests.get("http://127.0.0.1:5000/api/v1/register", headers={"User-Agent": "NoelP X - Python Requests","X-Eric-Cartman": getKey(),"username": username,"password": password})
    except requests.exceptions.ConnectionError: print("Server is down...")
    except: print("Unknown error..."); input(); exit(0)
    return r.json()["Success"]
def admin(apikey, username) -> str:
    try: r = requests.post("http://127.0.0.1:5000/api/v1/admin", headers={"User-Agent": "NoelP X - Python Requests","X-Eric-Cartman": getKey(),"username": username, "apikey": apikey})
    except requests.exceptions.ConnectionError: print("Server is down...")
    except: print("Unknown error..."); input(); exit(0)
    finally: return(r.json()["Message"], True) if r.json()["Success"] else (r.json()["Message"], False)
if __name__ == "__main__":
    print(getKey())
    print(
    """
    [Welcome to NoelP X!]
        [1]. Login
        [2]. Register
        [3]. Admin
    """
    )
    choice = input("Choice: ")
    if choice == "1":
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        print(login(username, password))
    elif choice == "2":
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        if register(username, password): print("Registered!")
        else: print("Username already taken!")
    elif choice == "3":
        apikey = input("API: ")
        username = input("Username: ")
        print(admin(apikey, username))