# Weather MCP Server

This is a sample MCP (Messaging and Compute Platform) server for a weather application, designed for the Puch AI Hackathon. It provides a basic structure for integrating with a weather API and includes the required `validate` and `resume` endpoints.

## Prerequisites

Before you begin, ensure you have the following installed:

*   [Python 3.9+](https://www.python.org/downloads/)
*   [Docker](https://www.docker.com/get-started) (for containerized deployment)
*   An API key from a weather service provider like [OpenWeatherMap](https://openweathermap.org/api).

## Getting Started

Follow these steps to get the project up and running on your local machine.

### 1. Clone the repository

```bash
git clone <repository_url>
cd weather_mcp
```

### 2. Set up environment variables

The application requires a `WEATHER_API_KEY` to be set as an environment variable.

**On macOS/Linux:**

```bash
export WEATHER_API_KEY='your_weather_api_key'
export MY_NUMBER='919876543210'
```

**On Windows:**

```powershell
$env:WEATHER_API_KEY='your_weather_api_key'
$env:MY_NUMBER='919876543210'
```

Alternatively, you can create a `.env` file in the root of the project and add the following lines. The `.gitignore` file is already configured to ignore this file.

```
WEATHER_API_KEY='your_weather_api_key'
MY_NUMBER='919876543210'
```
*Note: The current `app.py` does not automatically load `.env` files. You would need to add a library like `python-dotenv` for that. Also, make sure to replace `919876543210` with your actual phone number in the required format.*


### 3. Install dependencies

It's recommended to use a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 4. Run the application

```bash
flask run
```

The server will start on `http://127.0.0.1:5000`.

## Deployment to Render

This project is ready to be deployed to [Render](https://render.com/) using Docker.

1.  **Push your code to a GitHub repository.**
2.  **Create a new "Web Service" on Render** and connect it to your GitHub repository.
3.  **Choose the "Docker" environment.** Render will automatically detect the `Dockerfile`.
4.  **Add your `WEATHER_API_KEY`** as an environment variable in the Render dashboard.
5.  **Deploy!** Render will build and deploy your application. You will get a public URL for your service.

## API Endpoints

All endpoints are prefixed with `/mcp`.

### `/mcp`

*   **Method:** `GET`
*   **Description:** A simple endpoint to check if the server is running.
*   **Response:**
    ```json
    {
      "message": "Welcome to the Weather MCP server!"
    }
    ```

### `/mcp/get_current_weather`

*   **Method:** `POST`
*   **Description:** Gets the current weather for a city.
*   **Request Body:**
    ```json
    {
      "city": "London"
    }
    ```
*   **Response:** The JSON response from the OpenWeatherMap API.

### `/mcp/get_weather_forecast`

*   **Method:** `POST`
*   **Description:** Gets the weather forecast for a city.
*   **Request Body:**
    ```json
    {
      "city": "Paris",
      "days": 3
    }
    ```
*   **Response:** The JSON response from the OpenWeatherMap API.

### `/mcp/validate`

*   **Method:** `POST`
*   **Description:** A placeholder for the hackathon's `validate` endpoint.
*   **Request Body:**
    ```json
    {
      "phone_number": "1234567890",
      "resume_summary": "A brief summary of a resume."
    }
    ```

### `/mcp/resume`

*   **Method:** `POST`
*   **Description:** A placeholder for the hackathon's `resume` endpoint.
*   **Request Body:** (Currently none)

## Connecting to Puch AI

Once deployed, you should be able to connect your MCP server to Puch AI using the command mentioned in the hackathon instructions. It will likely be something like this, executed in WhatsApp:

```
/mcp connect <your_render_url>/mcp <your_auth_token>
```

Make sure to replace `<your_render_url>` with the URL provided by Render and `<your_auth_token>` with the token provided by the hackathon organizers. Always refer to the official hackathon documentation for the exact command and procedure.
