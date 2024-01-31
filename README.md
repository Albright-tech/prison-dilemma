# prison-dilemma
#GROUP PROJECT
# Prisoner's Dilemma Flask Application

This Flask application allows users to sign up, log in, and participate in a Prisoner's Dilemma scenario. Users can make decisions in the game, and the application provides endpoints for CRUD operations on decisions.

## Table of Contents

- [Setup](#setup)
- [Database Models](#database-models)
- [User Authentication](#user-authentication)
- [Prisoner's Dilemma Logic](#prisoners-dilemma-logic)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Group Members](#group-members)

## Setup

The application initializes Flask, sets up the SQLAlchemy database, bcrypt for password hashing, CORS for cross-origin resource sharing, and JWT (JSON Web Tokens) for user authentication.

## Database Models

### User

Represents users with attributes like username, email, and password.

### Decision

Represents decisions made in the Prisoner's Dilemma game, with attributes for player decisions and the game result.

## User Authentication

- `signup()` route: Allows users to register by providing a username, email, and password. Passwords are hashed using bcrypt before being stored in the database.
- `login()` route: Handles user login by checking credentials against the database and generating a JWT token upon successful authentication.
- `protected()` route: Demonstrates a protected endpoint that requires JWT authentication. Users must include their JWT token in the request headers to access this route.

## Prisoner's Dilemma Logic

- `prisoner_dilemma()` function: Implements the logic for the Prisoner's Dilemma game. It takes the decisions of two players and returns the outcome based on their choices.
- `/decision` route: Provides options for player decisions ('cooperate' or 'defect').
- `/decisions` routes:
  - `create_decision()`: Allows users to make decisions in the Prisoner's Dilemma game. It calculates the outcome and stores the decision in the database.
  - `read_decision()`: Retrieves all decisions made in the game from the database.
  - `update_decision()`: Allows users to update a decision by providing a decision ID and new player decisions.
  - `delete_decision()`: Allows users to delete a decision by providing its ID.

## Running the Application

The application runs with debug mode enabled (`python3 app.py`), allowing for automatic reloading and debugging.

## Testing

Users can interact with the API using tools like Postman. They can sign up, log in, make decisions, and perform CRUD operations on decisions.
## languages
python
javascript

## libraries
flask 
react



## Group Members

- Zakaria Mohammed
- Michelle Chemutai
- Albright Muchori
- Eric Wachiuri
- Nuru Amudi
- Faith Adline
- Ivy Ngatia
-kevin Kamadi


