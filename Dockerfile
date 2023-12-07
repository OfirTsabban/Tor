# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY server/main.py /app

# Install any needed packages specified in requirements.txt
RUN pip install cryptography

# Make port 3009 available to the world outside this container
#EXPOSE 3009

# Run app.py when the container launches
CMD ["python", "/app/main.py"]