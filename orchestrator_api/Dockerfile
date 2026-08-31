FROM python:3.12-bookworm

WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY orchestrator_api/requirements.txt ./orchestrator_api/requirements.txt
RUN pip install -r orchestrator_api/requirements.txt

COPY . .

CMD ["uvicorn", "orchestrator_api.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
