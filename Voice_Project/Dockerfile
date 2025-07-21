# Use official Python image
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy all project files to the container
COPY . .

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
