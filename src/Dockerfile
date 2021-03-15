FROM python:3.8

COPY . app/
WORKDIR /app/
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]