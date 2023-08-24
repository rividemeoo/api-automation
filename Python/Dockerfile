# Use an official Python runtime as the base image
FROM python:3.9

# Update package lists and install prerequisites
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-get update && \
    apt-get install -y unixodbc-dev

# Set the working directory in the container
WORKDIR /PythonApp

# Copy the contents of your local directory to the container
COPY . /PythonApp

# Install dependencies if you have any (requirements.txt)
RUN python -m pip install -r requirements.txt

# Run the pytest command when the container starts
CMD ["python", "-m", "pytest"]