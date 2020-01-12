FROM jomjol/raspberry-opencv-tensorflow

RUN [ "cross-build-start" ]

WORKDIR /

COPY . ./
RUN pip3 install --no-cache-dir -r requirements_raspi.txt

RUN [ "cross-build-end" ]

EXPOSE 3000

CMD ["python3", "./wasseruhr.py"]
