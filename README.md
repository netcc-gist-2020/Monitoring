# Monitoring Server

```
docker-compose up --build
```

socket server should be running.

for now setting run kvm09 server.

```
source /Monitoring/venv/bin/activate
python /Monitoring/server.py
```


```
docker run -dit --network=host --name datacenter datacenter
docker run -dit --network=host --name monitoring monitoring
docker run -dit --network=host --name db influxdb
```

network communicate within itself.
