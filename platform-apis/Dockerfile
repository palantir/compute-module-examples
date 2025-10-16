FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

RUN adduser --uid 5001 user
USER 5001

COPY src .

ENTRYPOINT ["python", "app.py"]
