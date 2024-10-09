# Full-stack Async Exercise

## 📄 Description

This project sets up the initial structure of a chatbot application using **FastAPI** for the backend. It currently includes:

- A health check route (`/health`) to monitor the application's status.
- **User Registration Endpoint** (`/users/register`) to allow users to create accounts.
- **User Login Endpoint** (`/users/login`) to enable users to authenticate. Authentication tokens are stored securely in HTTP-only cookies.
- **User Logout Endpoint** (`/users/logout`) to allow users to log out by clearing authentication cookies.
- **User Info Endpoint** (`/users/me`) to retrieve information about the currently authenticated user.
- **Protected `/messages` Endpoints** (`/messages`) to manage chatbot messages, accessible only to authenticated users. These endpoints allow users to:
  - **List Messages** (`GET /messages/`): Retrieve a list of messages sent and received.
  - **Send a Message** (`POST /messages/`): Send a new message to the chatbot.
  - **Edit a Message** (`PUT /messages/{id_message}`): Edit an existing user message.
  - **Delete a Message** (`DELETE /messages/{id_message}`): Delete a user message.

Additionally, the project has been refactored to enhance maintainability and scalability by:

- **Centralizing Configuration** in a dedicated `config.py` module.
- **Separating Models** into individual files within the `models` directory.
- **Organizing Utility Functions** within the `utils` directory.
- **Implementing Comprehensive Logging** within the authentication process for better monitoring and debugging.

This setup serves as a foundation for developing additional chatbot functionalities such as sending, editing, and deleting messages, as well as integrating more advanced chatbot logic.

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

- **Deployment:**
  - AWS App Runner
  - AWS Elastic Container Registry (ECR)

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
│   │   ├── messages.py
│   │   └── users.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── messages.py
│   │   └── users.py
│   └── utils/
│       ├── __init__.py
│       └── auth.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_health.py
│   ├── test_messages.py
│   └── test_users.py
├── .pre-commit-config.yaml
├── requirements.txt
├── Dockerfile
└── .gitignore
```

- **app/config.py**: Centralized configuration module loading environment variables.
- **app/main.py**: Entry point of the FastAPI application with logging configuration.
- **app/models/users.py**: Contains Pydantic models for user registration and login.
- **app/models/messages.py**: Contains Pydantic models for message management.
- **app/routers/users.py**: Defines the user registration, login, logout, and user info endpoints.
- **app/routers/messages.py**: Defines protected endpoints for managing chatbot messages (list, send, edit, delete).
- **app/routers/health.py**: Defines the `/health` route for health checks.
- **app/utils/auth.py**: Contains utility functions, including `get_secret_hash` for AWS Cognito and authentication dependencies.
- **tests/test_users.py**: Unit tests for user registration, login, logout, and user info endpoints.
- **tests/test_messages.py**: Unit tests for message management endpoints.
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
COGNITO_ISSUER=https://cognito-idp.<region>.amazonaws.com/<user_pool_id>
DYNAMO_MESSAGES_TABLE=Messages
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
```

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

### 7. Testing User Registration, Login, Logout, and Message Management

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
      "message": "Login successful"
    }
    ```
  - **Note:** Tokens are now stored in HTTP-only cookies. They are **not** returned in the response body for enhanced security.

- **User Logout:**
  - **Endpoint:** `POST /users/logout`
  - **Response:**
    ```json
    {
      "message": "Logout successful"
    }
    ```

- **Get Current User:**
  - **Endpoint:** `GET /users/me`
  - **Response:**
    ```json
    {
      "email": "newuser@example.com"
    }
    ```

- **List Messages:**
  - **Endpoint:** `GET /messages/`
  - **Response:**
    ```json
    {
      "messages": [
        {
          "id_message": "aee86f6d-26e0-4b77-a8be-44829d0e6e04",
          "id_user": "test-user-id",
          "content": "Hello!",
          "timestamp": "2024-10-07T07:33:21.023112",
          "is_bot": false
        },
        {
          "id_message": "31101aad-c65f-41b4-8210-a27649aaa124",
          "id_user": "test-user-id",
          "content": "Hi there!",
          "timestamp": "2024-10-07T07:35:21.023112",
          "is_bot": true
        }
        // ... other messages ...
      ]
    }
    ```

- **Send a Message:**
  - **Endpoint:** `POST /messages/`
  - **Payload:**
    ```json
    {
      "content": "Hello, chatbot!"
    }
    ```
  - **Response:**
    ```json
    {
      "user_message": {
        "id_message": "aee86f6d-26e0-4b77-a8be-44829d0e6e04",
        "id_user": "test-user-id",
        "content": "Hello, chatbot!",
        "timestamp": "2024-10-07T07:33:21.023112",
        "is_bot": false
      },
      "bot_response": {
        "id_message": "31101aad-c65f-41b4-8210-a27649aaa124",
        "id_user": "test-user-id",
        "content": "This is a bot response.",
        "timestamp": "2024-10-07T07:35:21.023112",
        "is_bot": true
      }
    }
    ```

- **Edit a Message:**
  - **Endpoint:** `PUT /messages/{id_message}`
  - **Payload:**
    ```json
    {
      "content": "Updated message content."
    }
    ```
  - **Response:**
    ```json
    {
      "id_message": "aee86f6d-26e0-4b77-a8be-44829d0e6e04",
      "content": "Updated message content."
    }
    ```

- **Delete a Message:**
  - **Endpoint:** `DELETE /messages/{id_message}`
  - **Response:**
    ```json
    {
      "id_message": "aee86f6d-26e0-4b77-a8be-44829d0e6e04",
      "status": "deleted"
    }
    ```

## 🧪 Running Tests

Ensure all development dependencies are installed and run:

```bash
pytest tests/
```

This command will execute all unit tests for user registration, login, and protected message routes, ensuring the reliability of authentication and authorization mechanisms.

### 📌 **Test Coverage**

- **Authentication Tests:**
  - Accessing protected routes without a token.
  - Accessing protected routes with an invalid token.

- **User Tests:**
  - Registering a new user.
  - Logging in with valid credentials.
  - Logging in with invalid credentials.

- **Message Tests:**
  - Listing messages for an authenticated user.
  - Sending a new message.
  - Editing an existing message.
  - Deleting a message.

## 🐳 Containerization with Docker

### 1. Build the Docker Image

```bash
docker build -t async-chatbot-api .
```

### 2. Run the Docker Container

```bash
docker run -d --name async-chatbot-api-container -p 8000:8000 --env-file .env async-chatbot-api
```

The application will be accessible at [http://localhost:8000](http://localhost:8000).

## 🔧 Deployment with AWS App Runner and ECR

### 1. Push Docker Image to AWS ECR

Ensure you have an AWS account and have configured the AWS CLI with appropriate permissions.

#### 1.1. Create an ECR Repository

```bash
aws ecr create-repository --repository-name async-chatbot-api --region your-region
```

#### 1.2. Authenticate Docker to Your ECR Repository

```bash
aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com
```

#### 1.3. Tag Your Docker Image

```bash
docker tag async-chatbot-api:latest your-account-id.dkr.ecr.your-region.amazonaws.com/async-chatbot-api:latest
```

#### 1.4. Push the Image to ECR

```bash
docker push your-account-id.dkr.ecr.your-region.amazonaws.com/async-chatbot-api:latest
```

### 2. Deploy with AWS App Runner

#### 2.1. Create an App Runner Service

Navigate to the AWS App Runner console and create a new service:

1. **Source**: Select "Container registry" and choose "Amazon ECR".
2. **Repository**: Select your `async-chatbot-api` repository and the `latest` tag.
3. **Service Settings**: Configure the service name, CPU, memory, and other settings as needed.
4. **Environment Variables**: Set the required environment variables as defined in your `.env` file.
5. **Networking**: Configure VPC, subnets, and security groups as necessary.
6. **Deployment**: Review and create the service.

The service will be deployed and accessible via the provided App Runner URL.

#### 2.2. Update Environment Variables

Ensure all necessary environment variables are set in the App Runner console under the service settings. These should mirror those in your local `.env` file but should be securely managed within AWS.


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

## 🛠️ Running Tests with Mocks

The tests utilize **pytest** and **FastAPI's TestClient** along with **unittest.mock** to simulate interactions with DynamoDB and the authentication process. This ensures that tests are isolated, fast, and do not depend on external services.

### 1. Install Test Dependencies

Ensure that **pytest** and **unittest.mock** are installed. These should already be included in your `requirements.txt`, but verify:

```bash
pip install pytest
```

### 2. Run the Tests

Execute all tests within the `tests/` directory:

```bash
pytest tests/
```

## 📝 **Notes**

- **Development Environment:** It's recommended to use a virtual environment to isolate project dependencies.
- **Docker:** Ensure Docker is installed on your machine to utilize containerization features.
- **Endpoint Testing:** Use tools like **Postman** or **cURL** to test API endpoints.
- **Security:**
  - Never commit sensitive information such as AWS credentials or Cognito secrets. Always use environment variables and ensure `.env` is listed in `.gitignore`.
  - In production, set `secure=True` for cookies to enforce HTTPS.
  - Consider implementing CSRF protection mechanisms since cookies are used for authentication.