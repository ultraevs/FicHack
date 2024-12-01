FROM python:3.11.5
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY . .
RUN mkdir uploaded_images
RUN python -m pip install -r requirements.txt
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8200"]