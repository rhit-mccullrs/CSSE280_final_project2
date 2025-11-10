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

def get_list_data(list_name):
    lists = get_lists("luke")
    list_data = {}
    list = lists[list_name]
    for x in list:
        list_data[x] = list[x]

    return list_data

def add_player(username, user_list, player, rating):
    db = get_db()
    user = db.get(username)
    user[user_list][player] = rating
    db.set(username,user)
    db.save()

def get_round_robin_pairings(data, current_round):
    pairings = {}
    players = []
    for key in data:
        players.append(key)
    num_players = len(players)
    # Handling odd number of players, so one gets a BYE
    if num_players % 2 == 1:
        pairings[players[(num_players-current_round)%num_players]] = "BYE"
        players.remove(players[(num_players-current_round)%num_players])
        num_players -= 1

    if(num_players == 0):
        return pairings
    
    arr = players[1:num_players//2] + list(reversed(players[num_players//2:num_players]))
    ref_arr = arr.copy()
    
    # do algorithm current_round times
    for i in range(current_round - 1):
        for j in range(len(arr)):
            arr[(j+1)%(num_players-1)] = ref_arr[j]
        ref_arr = arr.copy()

    # get top and bottom lists to do pairings
    top = arr[0:num_players//2-1]
    top0 = players[0]
    bottom = list(reversed(arr[(num_players-1)//2:(num_players-1)]))
    bot0 = bottom.pop(0)

    if current_round % 2 == 0:
        pairings[top0] = bot0
    else:
        pairings[bot0] = top0
    
    for i in range(len(top)):
        pairings[top[i]] = bottom[i]

    return pairings