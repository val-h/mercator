FROM python:3.9

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR ~/mercator/

# Install dependencies
COPY Pipfile Pipfile.lock /mercator/
RUN pip install pipenv && pipenv install

# Copy project
COPY . /mercator/
