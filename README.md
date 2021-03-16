# What is this?

Example webservice with FastAPI-uvicorn webserver and celery worker using a redis broker and backend.

# How do I try it out?

```
docker-compose up
```

Then make a request to the `/task` endpoint. It will then let you know which endpoint to poll for the result.

The API returns 202 Accepted until eventually a 307 redirect and a 200 OK with the result of the task.

[This pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/async-request-reply) is implemented.
