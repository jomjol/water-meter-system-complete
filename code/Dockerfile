FROM python:3.7

WORKDIR /

COPY ./tensorflow ./tensorflow
RUN pip install --no-cache-dir ./tensorflow/tensorflow-2.0.0-cp37-cp37m-linux_x86_64.whl
RUN rm -r ./tensorflow

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
RUN rm -r ./tensorflow

EXPOSE 3000

CMD ["python", "./wasseruhr.py"]
