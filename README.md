# Login Portal Demo

This README file provides instructions on how to run a demo of the login portal functionality that we've programmed.

## Prerequisites

Before running the demo, ensure that you have the following installed:

- Python 3.x
- Flask
- Werkzeug

You can install Flask and Werkzeug using the following command:

```
pip install flask werkzeug
```

## Files

The login portal consists of the following files:

- `app.py`: The main Flask application file that handles the routes and logic.
- `database.py`: The file that contains the database connection and user-related functions.
- `base.html`: The base template file that defines the common structure and layout.
- `login.html`: The template file for the login page.
- `register.html`: The template file for the registration page.
- `styles.css`: The CSS file that contains the styles for the login portal.

## Steps to Run the Demo

1. Clone the repository or download the files to your local machine.

2. Open a terminal or command prompt and navigate to the project directory.

3. Run the following command to start the Flask development server:

   ```
   python app.py
   ```

   This will start the server and display the URL where the application is running (e.g., `http://127.0.0.1:5000/`).

4. Open a web browser and visit the URL displayed in the terminal.

5. You will be redirected to the login page. If you don't have an account, click on the "Register here" link to go to the registration page.

6. On the registration page, enter a desired username and password, and click the "Register" button. If the registration is successful, you will be redirected to the login page.

7. On the login page, enter the registered username and password, and click the "Login" button. If the credentials are correct, you will be logged in and redirected to the home page.

8. On the home page, you will see a personalized welcome message with your username. The navigation menu will display a "Logout" link.

9. Click on the "Logout" link to log out of the application. You will be redirected back to the login page.

10. You can repeat the login and registration process with different usernames and passwords to test the functionality.

## Additional Notes

- The user data is stored in an SQLite database file named `users.db`. The database file will be created automatically when you run the application for the first time.

- Passwords are securely hashed and salted using the Werkzeug library before storing them in the database.

- The application uses Flask sessions to handle user authentication and maintain the logged-in state.

- The `styles.css` file contains basic styles for the login portal. You can modify the styles to customize the appearance of the pages.

That's it! You should now be able to run a demo of the login portal functionality. If you encounter any issues or have further questions, please let me know.
