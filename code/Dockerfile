FROM python:3.7

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 3000

CMD ["python", "./wasseruhr.py"]
