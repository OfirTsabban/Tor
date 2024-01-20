import sqlite3

def add_user(name, password, key, url):
    cur.execute("""INSERT INTO user VALUES(name, password, key, url)""")

def get_usernames():
    res = cur.execute("SELECT name FROM users")
    return res.fetchall()

def get_userpassword(name):
    res = cur.execute("SELECT password FROM users WHERE name = name")
    return res.fetchall()

def get_userkey(name):
    res = cur.execute("SELECT key FROM users WHERE name = name")
    return res.fetchall()

def get_userurl(name):
    res = cur.execute("SELECT url FROM users WHERE name = name")
    return res.fetchall()

def get_userip(name):
    url = get_userurl(name)
    index = url.find("//") +2
    url = url[index:]
    return url[:url.find(":")]

def get_userport(name):
    url = get_userurl(name)
    index = url.find("//") +2
    url = url[index:]
    index = url.find(":") +1
    url = url[index:]
    return url[:url.find("/'")]
