
# Alim Manage v2

Alim Manage v2 is a FastAPI-based application for managing nutrition and physical activity data.

## Features

- User management
- Food item tracking
- Meal logging
- Physical activity tracking
- Weight tracking

## Installation

1. Clone the repository:
git clone https://github.com/touremahi/alim_manage_v2.git cd alim_manage_v2


2. Create a virtual environment:
python -m venv venv source venv/bin/activate # On Windows, use venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt


4. Set up the database:
Configure your database connection in app/database.py


## Running the Application

To run the application, use the following command:

uvicorn app.main:app --reload

The API will be available at `http://localhost:8000`.

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

To run the tests, use the following command:

pytest

## Project Structure

- `app/`: Main application package
  - `main.py`: FastAPI application entry point
  - `database.py`: Database configuration
  - `models.py`: SQLAlchemy models
  - `schemas.py`: Pydantic schemas
  - `services.py`: Business logic and database operations
  - `routes.py`: API routes
- `tests/`: Test files
- `requirements.txt`: Project dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
