FROM jomjol/synology-opencv-tensorflow:tf21-cp36

WORKDIR /

COPY . ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["python", "./wasseruhr.py"]
