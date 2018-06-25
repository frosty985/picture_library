import pymysql

""" Functions for inserting/updating database """


def insert_file(cur, filename, data):
    """
    Insert file information into database
    :param cur;
    :param data;
    :return true/false:
    """
    """ first check current details are not already in database """
    sql = str("SELECT id FROM pictures WHERE filename = '{}'").format(filename)
    print("[Debug]\tRunning sql : " + str(sql))
    cur.execute(str(sql))
    print (cur.rowcount)
    if cur.rowcount == 0:
        sql = "INSERT into pictures "
        sql = sql + " (id, filename, orgdatetime, resolution, lat, lon, make, model, inserted, updated) "
        sql = sql + str(" VALUES (REPLACE(UUID(), '-', ''), '{}', '{}', '{}', '{}', '{}', '{}', '{}', NOW(), NOW())").format(filename, *data)
        print("[Debug]\tRunning sql : " + str(sql))
        cur.execute(str(sql))
    else:
        for row in cur:
            print(row)
