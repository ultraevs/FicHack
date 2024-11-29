FROM python:3.11.5
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY . .
RUN mkdir uploaded_images
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100"]