# Use an official Python runtime as a parent image
FROM python:3.6

# Pass the Github API token as build arg
ARG TOKEN

# Set the working directory to /app
WORKDIR /app
ENV PYTHONPATH=$(PWD):$PYTHONPATH
ENV PYTHONUNBUFFERED=TRUE
ENV GITHUB_API_TOKEN=$TOKEN

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run app.py when the container launches
CMD ["chalice", "local"]
