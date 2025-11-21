# AngoData API - AI Coding Agent Instructions

## Project Overview
This is a Flask-based REST API project named "AngoData API". Currently in early development stage with a minimal setup consisting of a single entry point (`app.py`).

## Tech Stack
- **Python**: 3.12.3
- **Web Framework**: Flask 3.1.2
- **Key Dependencies**: Werkzeug 3.1.3, Jinja2 3.1.6, Click 8.3.1

## Project Structure
```
angodata-api/
├── app.py          # Main Flask application entry point
└── venv/           # Python virtual environment (do not modify)
```

## Development Setup

### Environment Activation
Always activate the virtual environment before running any Python commands:
```bash
source venv/bin/activate
```

### Running the Application
The app runs in debug mode by default via:
```bash
python app.py
```
This starts the development server with debug=True for hot reloading.

### Installing New Dependencies
Use pip within the activated virtual environment:
```bash
source venv/bin/activate
pip install <package-name>
```

## Code Conventions

### Language & Messages
- **Portuguese**: User-facing messages and responses are in Portuguese (e.g., "AngoData API a funcionar!")
- Keep API responses and error messages in Portuguese unless specified otherwise

### Route Patterns
- Use Flask's route decorators with HTTP method shortcuts: `@app.get()`, `@app.post()`, etc.
- Return dictionary objects directly - Flask handles JSON serialization
- Example from `app.py`:
  ```python
  @app.get("/")
  def home():
      return {"message": "AngoData API a funcionar!"}
  ```

### Application Structure
- Single file architecture currently (`app.py`)
- Main Flask app instance: `app = Flask(__name__)`
- Direct execution: `if __name__ == "__main__":`

## Current Endpoints
- `GET /` - Health check endpoint returning status message in Portuguese

## Important Notes
- No git repository initialized yet - version control not in place
- No requirements.txt or other dependency management files - consider creating when adding new packages
- Debug mode is enabled - suitable for development but should be disabled for production
- No environment variables, configuration files, or database connections configured yet
