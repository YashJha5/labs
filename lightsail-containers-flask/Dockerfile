# Set base image (host OS)
FROM ubuntu:latest
RUN apt-get update && apt install python3 -y


# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN apt install python3-pip -y && pip install -r requirements.txt 

# Copy the content of the local src directory to the working directory
COPY flask_api.py .

# Specify the command to run on container start
CMD [ "python3", "./flask_api.py" ]