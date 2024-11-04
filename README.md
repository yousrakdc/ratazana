# Ratazana

Ratazana is a web application designed for sports enthusiasts, particularly fans of Nike jerseys. It offers users the ability to browse, like, and track prices of various jerseys, providing an intuitive interface for discovering and managing their favorite sports apparel.

## Features

- **User Authentication**: Secure registration and login using Django Allauth and JWT for token-based authentication.
- **Jersey Catalog**: View a comprehensive list of jerseys, complete with images, descriptions, sizes, and prices.
- **Price Tracker**: Monitor price changes and receive notifications when jerseys drop in price.
- **Likes**: Users can like jerseys, enabling them to keep track of their favorites.
- **Filter Options**: Filter jerseys by team, country, color, and price range for easier navigation.

## Technologies Used

- **Frontend**: 
  - React.js
  - React Router
  - CSS Modules

- **Backend**: 
  - Django
  - Django REST Framework
  - PostgreSQL

- **Other**: 
  - Celery for background tasks
  - Redis for caching
  - Docker for containerization

## Installation

To get a local copy up and running, follow these steps:

### Prerequisites

- [Node.js](https://nodejs.org/) (v14 or higher)
- [Python](https://www.python.org/) (v3.8 or higher)
- [PostgreSQL](https://www.postgresql.org/) (v12 or higher)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Clone the Repository

```bash
git clone https://github.com/yourusername/ratazana.git
cd ratazana
```

### Set Up the Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database settings in `backend/settings.py`. Update the DATABASES setting with your PostgreSQL credentials.

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

### Set Up the Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install the required packages:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

## Running Tests

To run tests for the backend:

```bash
python manage.py test
```

For the frontend, you can run:

```bash
npm test
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Django](https://www.djangoproject.com/) for the powerful backend framework
- [React](https://reactjs.org/) for creating dynamic user interfaces
- [Nike](https://www.nike.com/) for inspiring the project with their extensive catalog of jerseys


## Authors

- [@yousrakdc](https://www.github.com/yousrakdc)


