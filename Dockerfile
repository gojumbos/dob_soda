# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 7900
EXPOSE 80
#ENV PORT 9000

#ENV FLASK_APP app.py

# Run flask app when the container launches
# FLASK REQUIREMENT
#CMD ["flask", "run", "--host=0.0.0.0"]
#CMD ["python3", "app.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=7900"]


