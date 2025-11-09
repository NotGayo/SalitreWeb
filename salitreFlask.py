from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

def get_conn():
    return psycopg2.connect(os.getenv("SUPABASE_DB_URL"))

# ---------- vistas ----------
@app.route("/")
def index():
    return render_template("index.html")   # tu HTML sin tocar

# ---------- API ----------
@app.route("/api/reservas", methods=["GET"])
def listar():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, nombre, telefono, diaReserva, horaReserva::text, numComensales "
                "FROM Reserva ORDER BY diaReserva, horaReserva"
            )
            return jsonify(cur.fetchall())

@app.route("/api/reservas", methods=["POST"])
def crear():
    """
    Recibe el payload que envía el calendario (mismos nombres del formulario)
    y lo guarda en la tabla.
    """
    data = request.get_json(force=True)

    # Parsear la fecha y la hora que llegan juntas en "Fecha y hora"
    fecha_hora = data["Fecha y hora"]          # ej: "2025-11-15 13:30"
    dia, hora = fecha_hora.split(" ")

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO Reserva "
                "(nombre, telefono, email, numComensales, diaReserva, horaReserva, nota) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id",
                (
                    data["Nombre"],
                    data["Teléfono"],
                    data.get("Email") or None,
                    int(data["Personas"]),
                    dia,
                    hora,
                    data.get("Notas") or None
                )
            )
            conn.commit()
            return jsonify({"id": cur.fetchone()[0]}), 201

@app.route("/api/reservas/<int:id>", methods=["DELETE"])
def cancelar(id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Reserva WHERE id=%s", (id,))
            conn.commit()
            return jsonify({"ok": True})

# ---------- arrancar ----------
if __name__ == "__main__":
    app.run(debug=True)