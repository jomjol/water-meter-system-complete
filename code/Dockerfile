FROM jomjol/synology-opencv-tensorflow

WORKDIR /

COPY . ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["python", "./wasseruhr.py"]
