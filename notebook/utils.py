import mysql.connector
import clickhouse_connect

# Configuration MySQL
MYSQL_CONFIG = {
    "host": "mysql",
    "user": "user",
    "password": "password",
    "database": "testdb",
}

# Configuration ClickHouse
CLICKHOUSE_CONFIG = {
    "host": "clickhouse",
    "user": "default",
    "password": "password",
    "port": 8123,
}

client = clickhouse_connect.get_client(**CLICKHOUSE_CONFIG)
conn = mysql.connector.connect(**MYSQL_CONFIG)

# Connexion MySQL
def test_mysql():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(buffered=True)

    cursor.execute("DROP TABLE IF EXISTS test_table;")
    cursor.execute("""
        CREATE TABLE test_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name CHAR(10),
            value INT
        );
    """)

    cursor.execute("INSERT INTO test_table (name, value) VALUES ('test', 100), ('test', 200);")
    conn.commit()

    cursor.execute("SELECT * FROM test_table LIMIT 1;")
    print("MySQL :", cursor.fetchone())

    cursor.close()
    conn.close()


# Connexion ClickHouse
def test_clickhouse():
    client = clickhouse_connect.get_client(**CLICKHOUSE_CONFIG)

    client.command("DROP TABLE IF EXISTS test_table;")
    client.command("""
        CREATE TABLE test_table (
            id UInt32,
            name String,
            value Int32
        ) ENGINE = MergeTree()
        ORDER BY id;
    """)

    client.insert("test_table", [[1, 'test', 100], [2, 'test', 200]])

    result = client.query("SELECT * FROM test_table LIMIT 1;")
    print("ClickHouse :", result.result_rows[0])

def sql_query(query):
    """Fonction pour simplifier les requêtes mysql"""
    cursor = conn.cursor(buffered=True)
    cursor.execute(query)
    res = cursor.fetchall()
    cursor.close()
    return res