# Full-stack Async Exercise

## 📄 Description

This project sets up the initial structure of a chatbot application using **FastAPI** for the backend. It currently includes a health check route (`/health`) to monitor the application's status. This setup serves as a foundation for developing additional chatbot functionalities such as sending, editing, and deleting messages.

## 🚀 Technologies Used

- **Backend:**
  - Python 3.11.0
  - FastAPI
  - Uvicorn
  - Pytest

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
│   ├── main.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── health.py
├── tests/
│   ├── __init__.py
│   └── test_health.py
├── .pre-commit-config.yaml
├── requirements.txt
├── Dockerfile
└── .gitignore
```

- **app/main.py**: Entry point of the FastAPI application.
- **app/routers/health.py**: Defines the `/health` route for health checks.
- **tests/test_health.py**: Tests for the health check route.
- **.pre-commit-config.yaml**: Configuration file for pre-commit hooks.
- **requirements.txt**: Project dependencies.
- **Dockerfile**: Configuration for containerizing the application.
- **.gitignore**: Files and directories to be ignored by Git.

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

### 4. Set Up Pre-Commit Hooks

Ensure that **pre-commit** is installed and configured to run automatically before commits.

```bash
pre-commit install
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The application will be available at [http://localhost:8000](http://localhost:8000).

## 🧪 Running Tests

Ensure all development dependencies are installed and run:

```bash
pytest tests/
```

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


2. **Install the Git hooks:**

   ```bash
   pre-commit install
   ```

#### Usage

pre-commit hooks run automatically on `git commit`. To manually run all hooks against all files:

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