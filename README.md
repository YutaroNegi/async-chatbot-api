# Full-stack Async Exercise

## 📄 Description

This project sets up the initial structure of a chatbot application using **FastAPI** for the backend. It currently includes:

- A health check route (`/health`) to monitor the application's status.
- **User Registration Endpoint** (`/users/register`) to allow users to create accounts.
- **User Login Endpoint** (`/users/login`) to enable users to authenticate and receive authentication tokens.
- **Protected `/messages` Endpoints** (`/messages`) to manage chatbot messages, accessible only to authenticated users.

Additionally, the project has been refactored to enhance maintainability and scalability by:

- **Centralizing Configuration** in a dedicated `config.py` module.
- **Separating Models** into individual files within the `models` directory.
- **Organizing Utility Functions** within the `utils` directory.
- **Implementing Comprehensive Logging** within the authentication process for better monitoring and debugging.

This setup serves as a foundation for developing additional chatbot functionalities such as sending, editing, and deleting messages.

## 🚀 Technologies Used

- **Backend:**
  - Python 3.11.0
  - FastAPI
  - Uvicorn
  - Pytest
  - boto3
  - python-dotenv
  - python-jose

- **Containerization:**
  - Docker

- **Testing:**
  - pytest

- **Development Tools:**
  - Black
  - pre-commit

## 📂 Project Structure

```
async-chatbot-api/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── users.py
│   │   └── messages.py
│   └── utils/
│       ├── __init__.py
│       └── auth.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_health.py
│   ├── test_users.py
├── .pre-commit-config.yaml
├── requirements.txt
├── Dockerfile
└── .gitignore
```

- **app/config.py**: Centralized configuration module loading environment variables.
- **app/main.py**: Entry point of the FastAPI application with logging configuration.
- **app/models/user.py**: Contains Pydantic models for user registration and login.
- **app/routers/users.py**: Defines the user registration and login endpoints.
- **app/routers/messages.py**: Defines protected endpoints for managing chatbot messages.
- **app/routers/health.py**: Defines the `/health` route for health checks.
- **app/utils/auth.py**: Contains utility functions, including `get_secret_hash` for AWS Cognito and authentication dependencies.
- **tests/test_users.py**: Unit tests for user registration and login endpoints.
- **requirements.txt**: Project dependencies.
- **Dockerfile**: Configuration for containerizing the application.
- **.gitignore**: Files and directories to be ignored by Git.
- **.pre-commit-config.yaml**: Configuration file for pre-commit hooks.

## 🛠️ How to Run the Application Locally

### 1. Clone the Repository

```bash
git clone https://github.com/YutaroNegi/async-chatbot-api.git
cd async-chatbot-api
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

The application uses environment variables to manage sensitive configurations such as AWS Cognito settings. During development, these can be set using a `.env` file.

#### 4.1. Create a `.env` File

Create a `.env` file in the root directory with the following content:

```env
COGNITO_USER_POOL_ID=your_user_pool_id
COGNITO_APP_CLIENT_ID=your_app_client_id
COGNITO_APP_CLIENT_SECRET=your_app_client_secret
```

**Note:** Replace `your_user_pool_id`, `your_app_client_id`, and `your_app_client_secret` with your actual AWS Cognito configurations. Also, ensure that the `COGNITO_ISSUER` matches your Cognito User Pool's issuer URL.

#### 4.2. Secure the `.env` File

Ensure that the `.env` file is **not** committed to version control by keeping it listed in `.gitignore`.

### 5. Set Up Pre-Commit Hooks

Ensure that **pre-commit** is installed and configured to run automatically before commits.

```bash
pre-commit install
```

### 6. Run the Application

```bash
uvicorn app.main:app --reload
```

The application will be available at [http://localhost:8000](http://localhost:8000).

### 7. Testing User Registration and Login

- **User Registration:**
  - **Endpoint:** `POST /users/register`
  - **Payload:**
    ```json
    {
      "email": "newuser@example.com",
      "password": "Password123"
    }
    ```
  - **Response:**
    ```json
    {
      "message": "User created successfully"
    }
    ```
  - **Password Policy:**
    - Must be at least 8 characters long.
    - Must contain at least one number.

- **User Login:**
  - **Endpoint:** `POST /users/login`
  - **Payload:**
    ```json
    {
      "email": "newuser@example.com",
      "password": "Password123"
    }
    ```
  - **Response:**
    ```json
    {
      "access_token": "eyJraWQiOiJhb...",
      "id_token": "eyJraWQiOiJhb...",
      "refresh_token": "eyJjdHkiOi...",
      "token_type": "Bearer",
      "expires_in": 3600
    }
    ```


## 🧪 Running Tests

Ensure all development dependencies are installed and run:

```bash
pytest tests/
```

This command will execute all unit tests for user registration, login, and protected message routes, ensuring the reliability of authentication and authorization mechanisms.

## 🐳 Containerization with Docker

### 1. Build the Docker Image

```bash
docker build -t async-chatbot-api .
```

### 2. Run the Docker Container

```bash
docker run -d --name async-chatbot-api-container -p 8000:8000 async-chatbot-api
```

The application will be accessible at [http://localhost:8000](http://localhost:8000).

## 📑 Code Formatting and Linting

### Code Formatting with Black

This project uses [Black](https://github.com/psf/black) to ensure consistent code style.

#### Usage

Format all Python code in the project:

```bash
black app/ tests/
```

### Pre-Commit Hooks

[pre-commit](https://pre-commit.com/) is used to automatically run linting and formatting checks before each commit, ensuring code quality and consistency.

#### Installation

```bash
pre-commit install
```

#### Usage

Pre-commit hooks run automatically on `git commit`. To manually run all hooks against all files:

```bash
pre-commit run --all-files
```

## 🔧 Next Steps

- **Frontend:** Implement the user interface using **React** and **TypeScript**.
- **Chatbot Features:**
  - Send messages
  - Edit messages
  - Delete messages
- **Chatbot Logic:** Develop the chatbot logic to respond to user messages.
- **Data Persistence:** Add a persistence layer (e.g., database) to store messages.
- **Automated Testing:** Add more tests to cover new functionalities.
- **Deployment:** Configure continuous deployment using platforms like AWS Elastic Beanstalk.

---

### 📌 Additional Notes

- **Development Environment:** It's recommended to use a virtual environment to isolate project dependencies.
- **Docker:** Ensure Docker is installed on your machine to utilize containerization features.
- **Endpoint Testing:** Use tools like **Postman** or **cURL** to test API endpoints.