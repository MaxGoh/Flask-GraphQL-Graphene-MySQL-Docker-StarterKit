# Use an official Python runtime as an image
FROM python:3.7

# Copy all essentials file
COPY ./requirements.txt /usr/src/app/requirements.txt

# Work Directory
WORKDIR /usr/src/app

# Install requirements
RUN pip install -r requirements.txt

# Copy the rest
COPY . /usr/src/app

# Expose Port
EXPOSE 5000

# Start application
CMD [ "python", "manage.py", "runserver" ]
