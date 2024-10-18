# Django Task Management System API

This is a Django-based RESTful API for managing tasks and user assignments. It includes functionality for user authentication, task creation, and task management for both creators and executors.

## Models

### Task Model
- **creator**: Reference to the built-in User model, stores information about the creator of the task.
- **executor**: Reference to the built-in User model, stores information about the executor of the task. Can be empty.
- **name**: The name of the task (max length: 255 characters).
- **cost**: The cost of the task (decimal field, 8 digits total, 2 decimal places).
- **is_done**: Status of task completion (boolean).
- **deadline**: The deadline for task completion.

## Views

### 1. **UserCreateView**
- **POST**: Allows for the creation of a user.
  - Required fields: `username`, `password`, `email`.
  - Error responses:
    - 400 BAD REQUEST if any field is missing or if the username already exists.
  - Success response: 201 CREATED with user data (`id`, `username`, `email`).

### 2. **LoginView**
- **POST**: Authenticates a user and provides a token.
  - Required fields: `username`, `password`.
  - Error response: 401 UNAUTHORIZED if credentials are invalid.
  - Success response: 200 OK with the token (`{'token': <token_value>}`).

### 3. **LogoutView**
- **POST**: Logs the user out by deleting their authentication token.
  - Success response: 200 OK with a message (`{'message': 'Successfully logged out'}`).

### 4. **TaskCreateView**
- **POST**: Creates a new task with the authenticated user as the creator.
  - Required fields: `executor`, `name`, `cost`, `deadline`.
  - Error responses:
    - 400 BAD REQUEST if the creator is the executor.
    - 400 BAD REQUEST for invalid data.
  - Success response: 201 CREATED with the task's data.

### 5. **TasksCreatedByUser**
- **GET**: Displays tasks created by the authenticated user.
  - Fields: `executor`, `name`, `cost`, `deadline`.

### 6. **TaskWithExecutorAPIView**
- **GET**: Displays all tasks with executors.
  - If a task does not have an executor, `executor` is set to `"undefined"`.
  - Fields: `executor`, `name`, `cost`, `deadline`.

### 7. **UserTasksAPIView**
- **GET**: Displays tasks where the authenticated user is the executor.
  - Fields: `executor`, `name`, `cost`, `deadline`.

### 8. **UserTasksStatsAPIView**
- **GET**: Displays task statistics for the authenticated user.
  - Response fields:
    - `completed_tasks`
    - `pending_tasks`
    - `overdue_tasks`
    - `assigned_tasks`
    - `total_earned`: Sum of the cost of completed tasks.
    - `total_spent`: Sum of the cost of assigned tasks.
  - Example response:
    ```json
    {
      "completed_tasks": 0,
      "pending_tasks": 5,
      "overdue_tasks": 0,
      "assigned_tasks": 1,
      "total_earned": 0,
      "total_spent": 6000.0
    }
    ```

### 9. **UnassignedTasksAPIView**
- **GET**: Displays tasks without an assigned executor, sorted by cost (ascending).
  - Fields: `executor`, `name`, `cost`, `deadline`.

### 10. **BecomeExecutorAPIView**
- **PATCH**: Allows the user to become the executor of a task by providing the task ID in the URL.
  - Error responses:
    - 404 NOT FOUND if the task is not found.
    - 400 BAD REQUEST if the user is the creator or if the task already has an executor.
  - Success response: 200 OK with a message (`{'message': 'You have been assigned as the executor of the task'}`).

### 11. **MarkTaskDoneAPIView**
- **PATCH**: Allows the executor of a task to mark it as done by providing the task ID in the URL.
  - Error responses:
    - 404 NOT FOUND if the task is not found.
    - 400 BAD REQUEST if the user is not the executor.
  - Success response: 200 OK with the updated task data.

### 12. **ClearDatabaseView**
- **GET / POST**: Clears all tasks and users from the database for testing purposes.
  - Success response: 200 OK with a message (`{'message': 'All data cleared successfully'}`).

## Installation and Setup

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/task-management-api.git
```

### 2. Navigate to the project directory:
```bash
cd task-management-api
```
### 3. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```
### 4. Install the required dependencies:
```bash
pip install -r req.txt
```
### 5. Run the migrations:
```bash
python manage.py migrate
```
### 6. Create a superuser for admin access:
```bash
python manage.py createsuperuser
```
### 7. Run the development server:
```bash
python manage.py runserver
```
The API should be running locally, and you can access it at http://127.0.0.1:8000/.

## Configuration

### Setting Up the Secret Key

This project uses a secret key for cryptographic signing. You must configure this key for the application to run properly. Here’s how to set it up:

1. **Generate a Secret Key**: You can generate a new secret key using the following command:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   
2. **Create a .env File**: In the project root directory (where manage.py is located), create a file named ``.env``

3. **Add the Secret Key to the .env File**: Open the .env file and add the following line, replacing your-generated-secret-key with the key you generated:
```plaintext
DJANGO_SECRET_KEY='your-generated-secret-key'
```
4. **Add the .env File to .gitignore**: Ensure that the ``.env`` file is included in your ``.gitignore`` to prevent it from being pushed to GitHub, which could expose your secret key.
