# Ninja-Snap
Description

This application is designed to interface with Snapchat's advertising platform, enabling users to manage audience segments directly. It provides features to create, update, delete, and read segments, ensuring there is no duplication of segment names. The tool also allows for adding user identifiers to audience segments and tracks these insertions, updates, and deletions in a local SQLite database. It integrates authentication with Snapchat and handles environmental configurations easily.

Features

    Segment Management: Create, update, delete, and view segments without duplicating names.
    User Identifier Management: Add user identifiers to specific audience segments and ensure no duplications.
    Dashboard: A comprehensive dashboard to view all segments and possible actions.
    Logging: Detailed logging for app activities, API interactions, and database operations.
    Authentication: Handles OAuth2 authentication with Snapchat.
    Configuration Management: Easy management of environment variables through a configuration class.

Environment Configuration

The application uses the following environment variables set through the Config class:

    SQLALCHEMY_DATABASE_URI: Database connection string.
    TEMPLATES_DIR: Directory for Flask templates.
    LOGGING_DIR: Directory for log files.
    LOG_FILE_NAME: General application log file.
    API_LOG_FILE_NAME: API-specific log file.
    DB_LOG_FILE_NAME: Database operation log file.
    BASE_URL: Base URL for Snapchat's Ads API.
    TOKEN_URL: URL for obtaining OAuth tokens.
    AD_ACCOUNT_ID: Your Snapchat ad account ID.
    ORGANIZATION_ID: Your organization ID on Snapchat.
    CLIENT_ID: Your Snapchat application client ID.
    CLIENT_SECRET: Your application's client secret.
    REFRESH_TOKEN: OAuth refresh token for maintaining API access.

Setup and Installation
Prerequisites

    Python 3.x
    pip

Installation Steps

- Clone the repository:


    git clone https://github.com/KareemEmad98/Ninja-Snap.git

- Navigate to the project directory:


    cd Ninja-Snap

- Install the required dependencies:


    pip install -r requirements.txt

- Running the Application

    Set environment variables as described in the Config class.
    Run the Flask application:


    flask run

Usage

After starting the application, navigate to the local web address provided by Flask (usually http://127.0.0.1:5000/). The web interface allows full management of segments and user identifiers through intuitive forms and dashboard views.