FROM python:3.11-bookworm

WORKDIR /usr/src/habr_parser

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]