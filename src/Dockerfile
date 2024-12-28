### THIS DOCKERFILE IS FOR PRODUCTION ONLY.
### For development, use VS Code Dev container or Github Codespaces.

# Official Python image
FROM python:3.11.4-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ARG APP_USER=django
ARG APP_HOME=/home/${APP_USER}

# Update the install
RUN apt-get update && apt-get --no-install-recommends --yes upgrade && apt-get --no-install-recommends --yes install libpq5

# Set the working directory
WORKDIR $APP_HOME

# MAke sure we have a directory for media and static files.
RUN mkdir $APP_HOME/mediafiles
RUN mkdir $APP_HOME/staticfiles

# Update pip
RUN pip install --upgrade pip

# Install pip requirements
COPY requirements/requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

# Copy the source to the image
COPY . .

# Create the user and group and give user ownership to the files
RUN adduser --system --group ${APP_USER}
RUN chown -R ${APP_USER}:${APP_USER} ${APP_HOME}

# Make sure we don't run as root
USER $APP_USER

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]
