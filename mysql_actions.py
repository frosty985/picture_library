import pymysql

""" Functions for inserting/updating database """


def insert_file(cur, filename, data, debug=False):
    """
    Insert file information into database
    :param cur;
    :param data;
    :return true/false:
    """
    """ first check current details are not already in database """
    sql = str("SELECT id FROM pictures WHERE filename = '{}'").format(filename)
    if debug:
        print("[Debug]\tRunning sql : " + str(sql))
    cur.execute(str(sql))

    if cur.rowcount == 0:
        sql = "INSERT into pictures "
        sql = sql + " (id, filename, orgdatetime, resolution, lat, lon, make, model, inserted, updated) "
        sql = sql + str(" VALUES (REPLACE(UUID(), '-', ''), '{}', '{}', '{}', '{}', '{}', '{}', '{}', NOW(), NOW())").format(filename, *data)
        if debug:
            ("[Debug]\tRunning sql : " + str(sql))
        cur.execute(str(sql))

def get_pic_id(cur, filename, debug=False):
    sql = str("SELECT id FROM pictures WHERE filename = '{}'").format(filename)
    if debug:
        print("[Debug]\tRunning sql : " + str(sql))
    cur.execute(str(sql))
    row = cur.fetchone()
    while row is not None:
        if debug:
            print(filename + " is " + row["id"])
        return row["id"]
    else:
        return None

def get_con_id(cur, cat, debug=False):
    sql = str("SELECT id FROM contains WHERE contains.contains = '{}'").format(cat)
    if debug:
        print("[Debug]\tRunning sql : " + str(sql))
    cur.execute(str(sql))
    row = cur.fetchone()
    while row is not None:
        if debug:
            print("[Debug]\t" + cat + " is " + str(row["id"]))
        return row["id"]
    else:
        return None

def set_con(cur, filename, cat, debug=False):
    """
    Populate the pic_con table
    :param cur:
    :param filename:
    :param data:
    :return:
    """
    if debug:
        print("[Debug]\tGetting ids")
    cid = get_con_id(cur, cat, debug)
    pid = get_pic_id(cur, filename, debug)
    if debug:
        print("[Debug]\tGot cid='{}' pic='{}'".format(str(cid), str(pid)))

    if debug:
        print("[Debug]\tChecking if data is not already in database")
    if cid and pid:
        sql = "SELECT id FROM pic_con WHERE pid = '{}' AND cid = '{}'".format(str(pid), str(cid))
        cur.execute(sql)
        if cur.rowcount == 0:
            if debug:
                print("[Debug]\tData is already in database, skipping")
            sql = "INSERT INTO pic_con (id, pid, cid) VALUES (REPLACE(UUID(), '-', ''), '{}', '{}')".format(str(pid), str(cid))
            if debug:
                print("[Debug]\tRunning sql: ({})".format(sql))
                cur.execute(sql)