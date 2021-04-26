import psycopg2

db_host =  'database-2.cdmvj0zcuhga.us-east-2.rds.amazonaws.com'
db_name =  'postgres'
db_user =  'postgres'
db_pass =  'postgres'

def make_conn():
    str = "dbname='%s' user='%s' host='%s' password='%s'" % (db_name, db_user, db_host, db_pass)
    conn = psycopg2.connect(str)
    return conn


def fetch_data(conn, query, vars=None):
    result = []
    cursor = conn.cursor()
    print("Now executing: %s" % (cursor.mogrify(query, vars)))
    cursor.execute(query, vars)

    raw = cursor.fetchall()
    for line in raw:
        result.append(line)

    return result