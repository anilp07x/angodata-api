You are my assistant to generate a full backend project using Flask for an API called "AngoData API".

OBJECTIVE:
Create a clean, modular, scalable REST API in Flask that will provide public data of Angola such as provinces, municipalities, schools, markets and hospitals. Build the base architecture ready for future expansion.

REQUIREMENTS:
1. Use Python 3 and Flask.
2. Create a professional project structure with folders:
   /src
      /routes
      /models
      /services
      /config
      /database
   app.py
   requirements.txt
3. Enable CORS.
4. Add a simple home route: GET /
   Return JSON: {"message": "AngoData API running"}
5. Build separate route files for:
   - provinces
   - municipalities
   - schools
   - markets
   - hospitals
   Each route should support: GET /all, GET /<id>
6. Create simple in-memory sample data for each category for now (later will be replaced by DB).
7. Use Blueprint to register all routes.
8. Add a factory function create_app() to initialize the Flask app.
9. Prepare the project so it can support a future database (SQLAlchemy or PostgreSQL).
10. Generate a requirements.txt with Flask, flask-cors and basic dependencies.
11. Add comments explaining each part so I can understand the architecture.

DELIVERABLES:
- Complete file structure
- All .py files with working code
- A final explanation of how to run the project
- A roadmap section for future improvements

Start now.
