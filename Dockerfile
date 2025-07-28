# == state 1 ==
FROM python:3.10-alpine as builder

# setup
COPY ./src /app
COPY ./requirements.txt /app/
WORKDIR /app

# install requirements
RUN pip install --upgrade pip && pip install -U --no-cache-dir -r requirements.txt

# run __main__.py
CMD ["python", "."] 