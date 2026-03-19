# Service Engineering Project - AWS-based Repair Management

This project is a repair management platform built with Django and React, using AWS Rekognition, DynamoDB, and Step Functions.

### What it does
- Registers and logs in users by face.
- Creates repair requests and orchestrates workflow steps (approval, attendance, payment, pickup).
- Shows available appointments and tracking for repairs.

## Project structure

- `manage.py`: Django command-line entry.
- `ServicoAWS/`: Django project and API logic.
  - `api/views.py`: API endpoints.
  - `api/serializers.py`: data validation.
  - `api/dynamo.py`: DynamoDB access.
  - `api/rekognition.py`: face operations.
  - `api/stepfunction.py`: Step Functions calls.
  - `api/authentication.py`: token/auth helper.
- `React-shop-management/shop-management-react/`: frontend app.

## Backend setup

1. Create virtualenv and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Add env vars:
- `DJANGO_SECRET_KEY`
- AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`)
- `AWS_REGION`
- Step Function ARNs

3. Run database migrations:

```bash
python manage.py migrate
```

4. Start the server:

```bash
python manage.py runserver
```

## Architecture overview

The system has three main layers:

1. **Frontend (React)**
   - Single-page app in `React-shop-management/shop-management-react`.
   - User actions: sign up/login by face, request repair, track status, confirm pickup.
   - Uses `axios` to call backend REST endpoints.

2. **Backend (Django REST)**
   - Django project in `ServicoAWS/` with API views in `ServicoAWS/api/views.py`.
   - Each endpoint validates requests with serializers (`ServicoAWS/api/serializers.py`).
   - Core flow endpoints: face register/login, repair request, approval, attendance, payment, pickup, and status retrieval.

3. **AWS service integration**
   - **Rekognition** (`api/rekognition.py`): add/search faces using user images.
   - **DynamoDB** (`api/dynamo.py`): store users, requests, appointments, and task tokens.
   - **Step Functions** (`api/stepfunction.py`): drives long-running repair workflow and sends task tokens for human approvals.

### Data and workflow flow

- User registers a face image and gets a `face_id` stored in DynamoDB.
- Face login endpoint verifies identity via AWS Rekognition and returns JWT token.
- User creates a repair request: backend stores request and starts Step Function execution.
- Step Function orchestrates:
  1. Client approval (via token stored in DynamoDB)
  2. Staff attendance confirmation
  3. Repair execution and final payment confirmation
  4. Customer pickup confirmation
- Each action sends a callback to Step Functions with the task token.
- Repair status endpoint reads DynamoDB request item and returns the current state.

## Frontend setup

```bash
cd React-shop-management/shop-management-react
npm install
npm start
```

The app runs at `http://localhost:3000`.

## Main API routes

- `POST /api/face/register/`
- `POST /api/face/login/`
- `POST /api/repair/request/`
- `GET /api/repair/status/`
- `POST /api/approval/`
- `POST /api/staff/presence/`
- `POST /api/payment/confirm/`
- `POST /api/pickup/confirm/`
- `GET /api/appointments/`
- `GET /api/repairs/`
- `GET /api/users/`
