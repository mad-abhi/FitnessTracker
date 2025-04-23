# FitTrack - Fitness Tracking Application

FitTrack is a comprehensive fitness tracking web application built with Flask that helps users monitor their workouts, set fitness goals, and track their progress.

## Features

- **User Authentication**: Secure registration and login system
- **Dashboard**: Visual representation of workout stats and progress
- **Workout Tracking**: Log and manage workout sessions with details like duration, calories, and exercises
- **Exercise Library**: Browse through various exercises categorized by muscle groups
- **Goal Setting**: Create fitness goals with progress tracking
- **Profile Management**: Edit user profile and credentials

## Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Data Visualization**: Chart.js

## Getting Started

### Prerequisites

- Python 3.11 or higher
- PostgreSQL

### Installation

1. Clone the repository
   ```
   git clone https://github.com/mad-abhi/FitnessTracker.git
   cd FitnessTracker
   ```

2. Install required Python packages
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables
   ```
   export DATABASE_URL=postgresql://username:password@localhost/fittrack
   export FLASK_SECRET_KEY=your_secret_key
   ```

4. Run the application
   ```
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

## Application Structure

- `main.py`: Application entry point
- `models.py`: Database models
- `routes.py`: Application routes and views
- `forms.py`: Form validation and processing
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, and static assets

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)