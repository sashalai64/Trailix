# Trailix

## Overview
Trailix is a travel management web application designed to help users plan, track, and manage their trips seamlessly. Built using Django for the backend and JavaScript for dynamic front-end functionality, Trailix enables users to organize their travel itineraries and explore features like weather updates, countdown timers, city suggestions, and interactive maps.

## Features
- **User Authentication**
    - Secure login, logout, and registration functionality.
    - Personalized dashboard with user-specific trip details.

- **Trip Management**
    - Add trips with details like country, city, start date, end date, and notes.
    - View trips categorized as:
        - **Upcoming Trips**: Countdown timers display days left until the trip begins.
        - **Previous Trips**: Organized list of completed trips.
    - Automatic sorting of trips by start date for easy navigation.

- **Interactive Forms**
    - Dynamic city suggestions based on the selected country using external APIs.
    - Real-time form validation for required fields (e.g., city name).

- **Weather Integration**
    - Displays weather information for selected cities with icons for conditions like sun, clouds, and rain.
    - Cached weather data to reduce API calls and optimize performance.

- **Map Visualization**
    - An interactive map is displayed in the Previous Trips view, marking the cities of visited destinations.
    - Allows users to visually reflect on their travel history.

- **Responsive Design**
    - Fully responsive forms and pages that adapt to different screen sizes.

## Tech Stack
- Backend: Django, Python
- Frontend: HTML, CSS, JavaScript, AJAX
- APIs Used:
    - **Yahoo Weather API** for weather updates
    - **GeoDB Cities API** for location search and suggestions
    - **Google Time Zone API** for time zone data
- Database: SQLite
- Caching: Django cache framework (e.g., Memcached)

## Requirements
  - Python 3.x
  - Django

## Installation
1. **Clone the Repository**
      ```
      git clone https://github.com/sashalai64/trailix.git
      cd trailix 
      ```
      
2. **Set up environment variables**
    - Create a .env file in the project root directory.
    - Add your API keys and Django settings:
    ```    
    SECRET_KEY=<your-django-secret-key>  
    RAPID_GEODB_API_KEY=<your-rapid-geodb-api-key>  
    RAPID_WEATHER_API_KEY=<your-rapid-weather-api-key>  
    GOOGLE_CLOUD_API_KEY=<your-google-timezone-api-key>  
    DEBUG=True
    ```

3. **Apply Database Migrations**
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
   
4. **Run the Server**
      ```
      python manage.py runserver
      ```

5. **Access the Application**
    Visit `http://127.0.0.1:8000/` in your browser.

## Usage
1. **Sign Up**: Create a new account or log in with existing credentials.
2. **Add Trips**: Use the intuitive form to add upcoming or past trips.
3. **Explore Features**:
    - Check weather updates for trip locations.
    - View countdowns for upcoming trips.
    - Access city suggestions while entering trip details.