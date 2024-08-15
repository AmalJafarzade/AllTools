# Base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the wordlist into the container
COPY wordlist.txt /app
COPY jubey.txt /app

# Run the application
CMD ["python", "fuzz_dirsearch.py"]
