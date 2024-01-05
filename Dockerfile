FROM python:3.11

WORKDIR /app
COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv

RUN pipenv install --deploy --ignore-pipfile

COPY . /app

ENTRYPOINT ["pipenv", "run", "bash", "-c", "python main_app.py"]

