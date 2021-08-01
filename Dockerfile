FROM python:3.9

# Set env variables
# ENV PORT 8000
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

# Copy project
COPY . /code

# Run some command so the container doesn't shut down
CMD tail -f /dev/null

# For standalone docker image runnin, db doesn't work with this
# EXPOSE 8000
# CMD gunicorn --bind :8000 mercator.wsgi:application
