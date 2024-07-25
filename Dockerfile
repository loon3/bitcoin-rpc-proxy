# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Run script with a restart policy when the container launches
CMD ["sh", "-c", "until python proxy.py; do echo 'Restarting...'; sleep 1; done"]
