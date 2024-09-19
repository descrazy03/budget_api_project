# About The Project

**Description**

This project uses FastAPI to setup a very simple multi-user budgeting application. With this application, users can keep track of their income, expenses, and savings goals. An SQLite database is used to persist user data. 

**Details**

The application is based around four tables in the SQLite database and their respective FastAPI routers. The four tables are as follows:
- Users: contains usernames, passwords, first names, and last names of each user

- Categories: contains income and expense categories entered by users

- Records: contains dates, amounts, and brief descriptions for each transaction recorded by users
 
- Savings Goals: contains titles, amounts, and priorities for each savings goal entered by users

SQLAlchemy is used to interact with the database. Details about each table's FastAPI router can be found at http://127.0.0.1:8000/docs with the FastAPI application running.

# Installation and Setup
**Docker**

The easiest way to run the API would be to create an image from the Docker container. With Docker installed, run the follwing command to pull the image.

```
docker pull descrazy03/budgetapiproject
```

Run a container from the image and bind it to port 8000, then navigate to http://127.0.0.1:8000/docs to view the automatic documentation.

**Clone Repository**

You can also create a virtual environment and clone the repo.
```
insert github link here
```
Once the repository is cloned, run the following command:
```
fastapi run api_main.py
```
Then, navigate to http://127.0.0.1:8000/docs to view the automatic documentation.

## Usage
