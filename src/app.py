import os
from flask import Flask
import mysql.connector

app = Flask(__name__)

def get_db_conn():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "appuser"),
        password=os.getenv("MYSQL_PASSWORD", "apppass"),
        database=os.getenv("MYSQL_DATABASE", "appdb"),
    )

@app.get("/health")
def health():
    try:
        conn = get_db_conn()
        conn.close()
        return {"status": "ok"}, 200
    except Exception as e:
        return {"status": "error", "error": str(e)}, 500

@app.get("/")
def index():
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        # Tabla simple de visitas
        cur.execute("""
            CREATE TABLE IF NOT EXISTS visitas (
                id INT PRIMARY KEY AUTO_INCREMENT,
                ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("INSERT INTO visitas () VALUES ()")
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM visitas")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return f"Hola mundo! Conexión a MySQL exitosa. Visitas: {count}\n"
    except Exception as e:
        return (f"Error conectando a MySQL: {e}\n", 500)

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
