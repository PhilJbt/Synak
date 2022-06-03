#!/usr/bin/python3

import sqlite3

import sk__dbg

# Function to get a connection with the SQLITE database
def sql_con():
    # Open or create database
    dbPath = r'/synak_ms/wp_res/db/blacklist_uid.db'
    con = None
    try:
        con = sqlite3.connect(dbPath)
    except sqlite3.OperationalError:
        sk__dbg.message(sk__dbg.messtype.ERR, "Can't connect to /synak_ms/wp_res/db/blacklist_uid.db.")
        if con:
            con.close()
        return [None, False]

    # If table does not exist, create table
    cur = con.cursor()
    cur.execute("""SELECT count(name) FROM sqlite_master WHERE type='table' AND name='t_ban'""")
    if cur.fetchone()[0] == 0 :
        try:
            cur.execute("""CREATE TABLE if not exists t_ban(c_uid TEXT NOT NULL PRIMARY KEY, c_tim TEXT NOT NULL)""")
            con.commit()
        except sqlite3.Error as er:
            sk__dbg.message(sk__dbg.messtype.ERR, 'Error when creating table t_ban: %s' % (' '.join(er.args)))
            if con:
                con.close()
            return [None, False]

    return [con, True]

# Function to send sqlite request
def sql_req(_con, _req):
    res = None
    try:
        cur = _con.cursor()
        res = cur.execute(_req)
        _con.commit()
        res = cur.fetchall()
    except sqlite3.Error as er:
        sk__dbg.message(sk__dbg.messtype.ERR, f'Error when "{_req}": %s' % (' '.join(er.args)))
        if _con:
            _con.close()
        return [None, False]
    return [res, True]

#Function to close sqlite
def sql_cls(_con):
    # Close sqlite connection
    if _con :
        _con.close()
