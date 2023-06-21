FROM python:3.9

WORKDIR /app


COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire project code into the Docker image
COPY . .

# Expose the port on which your application listens
EXPOSE 8000

# Set the environment variables for the PostgreSQL database
ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_NAME=mydatabase
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword

# Run any necessary database migrations
RUN python manage.py migrate

# Copy the .env file into the Docker image
COPY .env .env

# Run the Python application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
