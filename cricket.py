from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__, template_folder="templates")

# MySQL Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Password",
    database="cricket_analysis"
)
cursor = conn.cursor()

# Power BI Dashboard Base URL
POWER_BI_BASE_URL = "https://app.powerbi.com/groups/me/reports/b2e21257-3077-47b9-a0b1-2b0f6c370b79?ctid=46bf6ae7-ea15-46bd-8443-1e18142e1da4&pbi_source=linkShare"

@app.route('/')
def home():
    return render_template("cricket.html")  # Yeh ab HTML file serve karega

@app.route('/search', methods=['GET'])
def search_player():
    player_name = request.args.get('player', '').strip()
    print("Received Player Name:", player_name)  # Debugging line

    if not player_name:
        return jsonify({"found": False, "message": "Player name is required"})
    
    query = "SELECT DISTINCT batter FROM ball_by_ball WHERE batter = %s"
    cursor.execute(query, (player_name,))
    result = cursor.fetchone()
    
    if result:
        return jsonify({"found": True, "dashboard_url": f"{POWER_BI_BASE_URL}&player={player_name}"})
    else:
        return jsonify({"found": False, "message": "Player not found"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
