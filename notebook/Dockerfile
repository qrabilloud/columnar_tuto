FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends

WORKDIR /dataset
COPY ./dataset /dataset

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
