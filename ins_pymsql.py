import pymysql

def fetch_one_sql(conn, sql, data=None):
    cursor = conn.cursor()
    cursor.execute(sql, data)
    result = cursor.fetchall()
    cursor.close()
    return result

def oprt_mysql(conn,sql,data=None):
    cursor = conn.cursor()
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()

if __name__ == "__main__":
    conn = pymysql.connect(host='localhost', port=3306,
                    user='root', password='123456',
                    db='xy_test', charset='utf8')
    sql = "select * from kh_name"
    date = fetch_one_sql(conn,sql)
    kh_name = []
    for i in date:
        kh_name.append(i[1])
    print(kh_name)