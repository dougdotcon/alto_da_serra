# Alto da Serra - Restaurant Management System

A desktop management system tailored for the 'Alto da Serra' restaurant, designed to streamline table tracking, order management, and payment processing.

## ✨ Features

*   **Table Management:** Open, close, and monitor the status of all tables in real-time.
*   **Order Processing:** Easily add consumption items to specific tables.
*   **Consumption Tracking:** View detailed logs of items consumed per table.
*   **Payment Handling:** Support for partial or full bill settlements.
*   **Intuitive Interface:** A clean dashboard designed for efficient daily operations.

## 🛠️ Technology Stack

*   **Frontend:** [Flet](https://flet.dev/) - Framework for building multi-platform applications in Python.
*   **Backend:** [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework for building APIs with Python.
*   **Server:** [Uvicorn](https://www.uvicorn.org/) - ASGI server used to run the FastAPI application.
*   **Database:** SQLite - A local file-based database (`restaurante.db`) is used to store all persistent data.

## 📂 Project Structure


alto_da_serra/
├── backend/
│   ├── api.py             # FastAPI logic and endpoints
│   ├── restaurante.db     # SQLite database file
│   └── ...
├── frontend/
│   ├── login.py           # Login screen
│   ├── painel.py          # Main dashboard after login
│   ├── components/        # UI components (Flet)
│   └── ...
├── requirements.txt       # Project dependencies
├── start_local.py         # Script to start the application locally
└── README.md


## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

*   [Python 3.8+](https://www.python.org/downloads/)

### Installation

1.  Clone the repository to your local machine.
2.  Navigate to the root directory of the project.
3.  Create and activate a virtual environment (recommended):
    bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    
4.  Install the required dependencies:
    bash
    pip install -r requirements.txt
    

### Running the Application

To start the backend and frontend simultaneously, run the `start_local.py` script:

bash
python start_local.py


The script will:
1.  Start the backend server at `http://127.0.0.1:8000`.
2.  Launch the desktop application (frontend).

## 🐳 Docker

The project can also be containerized using Docker. A `Dockerfile` is included in the root directory to build the necessary image.
*Implementation details pending.*
