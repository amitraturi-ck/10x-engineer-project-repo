# PromptLab

**Your AI Prompt Engineering Platform**

---

## Project Overview

PromptLab is a cutting-edge platform designed for AI engineers to handle and refine AI prompts. It's akin to a "Postman for Prompts," offering a suite of tools for managing, organizing, and optimizing AI prompts effectively. This platform aims to streamline the workflow of AI developers by providing an intuitive environment for prompt engineering needs.

### Purpose

The primary purpose of PromptLab is to centralize the storage of prompt templates, enable efficient organization into collections, facilitate seamless searching and tagging, and allow version tracking, all while being integrated into a robust development and deployment ecosystem.

---

## Features List

- **Prompt Management**: Store and manage prompt templates with dynamic variables.
- **Collections**: Organize prompts into cohesive collections.
- **Tagging and Searching**: Efficiently tag and search prompts within your workspace.
- **Version History**: Track changes and version history for each prompt.
- **API Access**: Expose a RESTful API for prompt operations.
- **CI/CD Integration**: Streamline deployment cycles (future development).
- **User Authentication**: Secure access to prompt data (future development).

---

## Prerequisites and Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd promptlab

# Set up backend
cd backend
pip install -r requirements.txt
```

---

## Quick Start Guide

To get started with PromptLab on your local machine:

1. **Run the Backend**:
   ```bash
   cd backend
   python main.py
   ```
   Your API will be live at [http://localhost:8000](http://localhost:8000)

2. **Access API Documentation**:
   Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI interactive documentation.

3. **Run Tests**:
   ```bash
   cd backend
   pytest tests/ -v
   ```

---

## API Endpoint Summary

| Method | Endpoint          | Description         |
|--------|-------------------|---------------------|
| GET    | `/health`         | Health check        |
| GET    | `/prompts`        | List all prompts    |
| GET    | `/prompts/{id}`   | Get single prompt   |
| POST   | `/prompts`        | Create prompt       |
| PUT    | `/prompts/{id}`   | Update prompt       |
| DELETE | `/prompts/{id}`   | Delete prompt       |
| GET    | `/collections`    | List collections    |
| POST   | `/collections`    | Create collection   |
| DELETE | `/collections/{id}` | Delete collection |

### Example: Fetch All Prompts
```bash
curl -X GET "http://localhost:8000/prompts" -H "accept: application/json"
```

---

## Development Setup

1. **Backend**:
   - Code is structured under `backend/app/` with FastAPI managing API routes and Pydantic for data validation.
   - Ensure Python dependencies are managed with `requirements.txt`.

2. **Frontend**:
   - Planned for development using React and Vite in subsequent project phases. 

3. **Testing**:
   - Run tests using `pytest` to ensure code quality and reliability.

4. **Continuous Integration/Deployment**:
   - Planned integration with Docker and GitHub Actions for seamless deployment workflows.

---

## Contributing Guidelines

We're excited to have a community of contributors who desire to build a robust and innovative platform.

1. **Fork the Repository**: Make your own version to work with.
2. **Create a Feature Branch**: Work on changes in feature-specific branches.
3. **Commit Changes**: Make and commit your changes with clear and concise messages.
4. **Push Branch**: Push your feature branch to your fork.
5. **Submit a Pull Request**: Open a pull request with a descriptive summary of your changes.

For major changes, please open an issue first to discuss what you would like to change.


