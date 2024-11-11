# Use the Python base image
FROM python:3.11.7


# Set working directory
WORKDIR /

# Copy requirements file
COPY requirements.txt .

# Install virtualenv
RUN python -m pip install --upgrade pip && \
    python -m pip install virtualenv

# Create a virtual environment and install dependencies there
RUN python -m virtualenv venv && \
    ./venv/bin/pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application within the virtual environment
CMD ["./venv/bin/python", "wsgi.py"]
