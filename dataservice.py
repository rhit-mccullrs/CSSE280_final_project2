import pickledb
import os

db_path = 'tournament.db'
global_db = None

def login(username, password):
    db = get_db()
    if username in db.all():
        if "password" not in db.get(username):
            return False
        return password==db.get(username["password"])
    return False

def create_account(username, password):
    db = get_db()
    db.set(username, {"password":password,
                      "lists": {}})
    db.save()

def load_db():
    global global_db
    db_file_already_exists = os.path.exists(db_path)
    global_db = pickledb.PickleDB(db_path)
    if not db_file_already_exists:
        global_db.set("luke", {"password": "1234",
                               "lists": {
                                   "rose-hulman": {
                                       "riley": 1842
                                   },
                                   "purdue": {
                                       "josh": 1912
                                   }
                                }
                                })
        global_db.save()

def get_db():
    global global_db
    if global_db is None:
        load_db()
    return global_db

def get_lists(username):
    db = get_db()
    all_lists = db.get(username)["lists"]
    lists = {}
    user = db.get(username)
    for x in all_lists:
        lists[x] = user["lists"][x]

    return lists

def get_list_data(username, list_name):
    lists = get_lists("luke")
    list_data = {}
    list = lists[list_name]
    for x in list:
        list_data[x] = list[x]

    return list_data
