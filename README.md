# wdt

Platform to create and share social Events. 
Based on a gRPC Django implementation.

## Requirements

- Python (3.6, 3.7, 3.8)
- Django (2.2, 3.0), Django REST Framework (3.10.x, 3.11.x)
- gRPC, gRPC tools, proto3

## Test / Use 

You can run a gRPC client to access the service:
```
$ python manage.py grpcrunserver --dev
```