# Setup of Cron job on Raspberry

In the current version of Tensorflow (2.0) is a memory leakage in the function tf.predict(). This causes especially on the Raspberry the docker container to crash after some time.
A work around for this is a regular restart of the container. The idea is from the user pfried from the iobroker forum - Many thanks to this!

## Implementation
The restart is done using within a cron job. To make this easier it is recommendet to give your docker container a dedicated name at start (```--name wasser```):

```docker run -d --name wasser -p 3000:3000 --mount type=bind,source=/PATH_TO_LOCAL_CONFIG, target=/config --mount type=bind,source=/PATH_TO_LOCAL_LOG,target=/log jomjol/wasserzaehler:raspi-latest```

After this you can easily restart it with a given frequency using a cron job in the file '''/etc/crontab''':

```0 */6 * * *   root    /usr/bin/docker restart wasser```
 
 In this example the container will be restartet every 6 hours on the full hour.
 
 Explanation for cron jobs on Raspberry Pi can be found [here](http://raspberry.tips/raspberrypi-einsteiger/cronjob-auf-dem-raspberry-pi-einrichten)

