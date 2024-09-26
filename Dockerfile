# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the relevant files from the local machine to the container
COPY ./app.py /app/app.py
COPY ./requirements.txt /app/requirements.txt
COPY ./ /app/

# Install the required Python packages
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ensure the 'database' directory exists in the container for SQLite
RUN mkdir -p /app/database

# Expose port 5003 to the outside world
EXPOSE 5003

# Run app.py when the container launches
CMD ["python", "/app/app.py"]