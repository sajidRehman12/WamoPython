# 1. Start with an official, lightweight Python base image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /code

# 3. Copy the requirements file into the container first
COPY ./requirements.txt /code/requirements.txt

# 4. Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copy the rest of your app's source code into the container
COPY ./main.py /code/main.py

# 6. Tell Docker the command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]