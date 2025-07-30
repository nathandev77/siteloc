from flask import Flask, request
from flask_cors import CORS
from datetime import datetime
import csv
import os

app = Flask(__name__)
CORS(app)  # Permite requisições de outros domínios (ex: Netlify)

ARQUIVO = "localizacoes.csv"

# Cria o arquivo se não existir
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["data_hora", "latitude", "longitude", "ip"])

@app.route("/api", methods=["POST"])
def salvar_localizacao():
    data = request.get_json()
    print("📦 JSON recebido:", data)

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    ip = request.remote_addr
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ARQUIVO, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([agora, latitude, longitude, ip])

    print(f"[{agora}] Localização salva: {latitude}, {longitude} | IP: {ip}")
    return "OK", 200

@app.route("/")
def status():
    return "Servidor online. Use /api para enviar dados de localização."

@app.route("/ver")
def ver_localizacoes():
    if not os.path.exists(ARQUIVO):
        return "<h2>Nenhuma localização salva ainda.</h2>"

    html = "<h2>Localizações Salvas</h2><table border='1' cellpadding='5'><tr><th>Data/Hora</th><th>Latitude</th><th>Longitude</th><th>IP</th></tr>"

    with open(ARQUIVO, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Pular o cabeçalho
        for row in reader:
            html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"

    html += "</table>"
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

