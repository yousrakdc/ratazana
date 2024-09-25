# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variable to skip Pyppeteer Chromium download (we will install it manually)
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true

# Install system dependencies (necessary for running Pyppeteer and Chromium)
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for Django development server
EXPOSE 8000

# Run the Django development server by default
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
