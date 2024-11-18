from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/send_coordinates/<int:x>/<int:y>', methods=['GET'])
def send_coordinates(x, y):
    # ESP32'ye veriyi gönder
    # Seri veya MQTT üzerinden bağlanabilirsiniz.
    return jsonify({"status": "success", "x": x, "y": y})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
