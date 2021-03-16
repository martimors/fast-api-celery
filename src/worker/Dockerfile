FROM python:3.8

COPY worker/ app/worker/
WORKDIR /app/
RUN pip install -r worker/requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "-m", "celery", "-A", "worker.tasks", "worker", "--loglevel=debug" ]