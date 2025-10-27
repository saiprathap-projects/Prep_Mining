FROM ubuntu:latest

WORKDIR /app

RUN  apt update -y && apt install -y \
     python3 \
     python3-pip \
     python3-venv \
     && rm -rf /var/lib/apt/lists/*
     
COPY requirements.txt .

COPY Prep_Mining /opt/Prep_Mining

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 5000
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "flaskapp.app:app"]