# Use an official Python runtime as a parent image
FROM python:3.8
ARG SCRIPT_NAME

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
RUN echo ${SCRIPT_NAME}

EXPOSE ${PORT_NUMBER}
# Run the appropriate python file when the container launches
CMD ["python", '\"${SCRIPT_NAME}\"']
