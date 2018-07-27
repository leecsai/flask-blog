import MySQLdb


def db_emp_insert(mysql_uri, cname, cpass, cemail, ccomp, cdepart, cbirth, csex, ctag):
    mysql_uri = mysql_uri
    list = list
    db = MySQLdb.connect(mysql_uri)
    cursor = db.cursor()
    sql = """ insert into emp(name, password, email, company, depart, birth, sex, tag) values(%s,%s,%s,%s,%s,%s,%s,%s) """
    try:
        cursor.executemany(sql, list)
        db.commit()
    except:
        #roll back in case there's an error
        db.rollback()
    db.close()

def db_emp_update(mysql_uri, key, value, number):
    mysql_uri = mysql_uri
    key = key
    value = value
    number = number
    sql = "update emp set " + key + "=" + value + " where id=" + str(number)
    db = MySQLdb.connect(mysql_uri)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

def db_emp_name_query(mysql_uri, qname):
    mysql_uri = mysql_uri
    qname = qname
    sql = 'select * from emp where name like "%' + qname + '%"'
    db = MySQLdb.connect(mysql_uri)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except:
        print("no user")
    db.close()

def db_emp_tag_query(mysql_uri, qtag):
    mysql_uri = mysql_uri
    qtag = qtag
    sql = 'select * from emp where tag like "%' + qtag + '%"'
    db = MySQLdb.connect(mysql_uri)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
    except:
        print("no user")
    db.close()

def db_emp_del(mysql_uri, name):
    mysql_uri = mysql_uri
    name = name
    db = MySQLdb.connect(mysql_uri)
    cursor = db.cursor()
    sql = """ delete from emp where name = '%s'""" % name
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()

