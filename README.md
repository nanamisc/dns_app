# AS Deployment


run
```
docker build -t nanamisc/auth_server ./AS
docker run -d -p 53533:53533/udp dns_app-auth_server
```

# FS Deployment

run
```
docker build -t nanamisc/fib_server ./FS
docker run -d -p 9090:9090 dns_app-fibonacci_server
```

# US Deployment

run
```
docker build -t nanamisc/user_server ./US
docker run -d -p 8080:8080 dns_app-user_server
```
