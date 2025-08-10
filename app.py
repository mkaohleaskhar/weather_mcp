import os
from flask import Flask, request, jsonify
import requests

# Initialize Flask app
app = Flask(__name__)

# Get environment variables.
# For local testing, you can set them in your terminal or a .env file.
# For production, set them in your deployment service's dashboard.

# ##############################################################################
# # SECURITY WARNING: HARDCODED KEYS FOR LOCAL TESTING ONLY                    #
# ##############################################################################
# # The following lines use hardcoded keys as a fallback.                      #
# # This is a temporary solution because of file system issues.                #
# #                                                                            #
# # ==> DO NOT COMMIT THIS TO A PUBLIC REPOSITORY. <==                         #
# # ==> REGENERATE THESE KEYS IF THEY ARE EVER EXPOSED. <==                    #
# ##############################################################################
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY') or '635dd241dfbb1c40bdd2a8f83e9d1c0a'
MY_NUMBER = os.environ.get('MY_NUMBER') or '919876543210' # Replace with your number
# ##############################################################################

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/"

if not os.environ.get('WEATHER_API_KEY'):
    print("Warning: Using hardcoded WEATHER_API_KEY for local testing.")
if not os.environ.get('MY_NUMBER'):
    print("Warning: Using hardcoded MY_NUMBER for local testing. Remember to replace it with your actual number.")

@app.route('/mcp')
def mcp_root():
    return jsonify({"message": "Welcome to the Weather MCP server!"})

@app.route('/mcp/get_current_weather', methods=['POST'])
def get_current_weather():
    """
    Gets the current weather for a given city.
    Expects a JSON payload with a 'city' key.
    """
    data = request.get_json()
    if not data or 'city' not in data:
        return jsonify({"error": "Missing 'city' in request body"}), 400

    city = data['city']

    if not WEATHER_API_KEY:
        return jsonify({"error": "Weather API key not configured"}), 500

    try:
        url = f"{WEATHER_API_URL}weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mcp/get_weather_forecast', methods=['POST'])
def get_weather_forecast():
    """
    Gets the weather forecast for a given city and number of days.
    Expects a JSON payload with 'city' and 'days' keys.
    The free OpenWeatherMap API provides a 5-day forecast with 3-hour granularity.
    """
    data = request.get_json()
    if not data or 'city' not in data:
        return jsonify({"error": "Missing 'city' in request body"}), 400

    city = data['city']
    # Note: 'days' is not directly used by the free API in the same way,
    # but we can use it to limit the results if needed.
    # The 'cnt' parameter can be used to limit the number of timestamps returned.
    # 5 days * 8 timestamps/day = 40 timestamps
    days = data.get('days', 5)
    cnt = days * 8

    if not WEATHER_API_KEY:
        return jsonify({"error": "Weather API key not configured"}), 500

    try:
        url = f"{WEATHER_API_URL}forecast?q={city}&appid={WEATHER_API_KEY}&units=metric&cnt={cnt}"
        response = requests.get(url)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mcp/validate', methods=['POST'])
def validate():
    """
    This is a mandatory endpoint required by Puch AI for server authentication.
    It must return the server owner's phone number in the format {country_code}{number}.
    The phone number is retrieved from the MY_NUMBER environment variable.
    """
    if not MY_NUMBER:
        return jsonify({"error": "Server owner's phone number is not configured"}), 500

    # Per the Puch AI documentation, this endpoint should return the phone number as a string.
    # The official starter kit returns it directly, not in a JSON object.
    # However, to maintain consistency with a JSON API, we will return it as a JSON string.
    # If this fails, consider returning the raw string: `return MY_NUMBER, 200`
    return jsonify(MY_NUMBER)

@app.route('/mcp/resume', methods=['POST'])
def resume():
    """
    This is a placeholder for the 'resume' endpoint mentioned in the hackathon description.
    The specific requirements for this endpoint are not detailed in the MCP documentation.
    You should implement its logic based on the hackathon's rules or your app's needs.
    It might be used to resume a conversation or a task.
    """
    return jsonify({
        "status": "resumed",
        "message": "Resume endpoint called successfully. Implement your logic here."
    })

if __name__ == '__main__':
    # The server will run on port 5000 by default.
    # You can change this by setting the PORT environment variable.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
