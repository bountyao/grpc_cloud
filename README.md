# CSC3004: Cloud and Distributed Computing

### **Team**: 24

### **Assignment**: Lab Assessment

### **Deadline**: 27 June 2022, 2359

| Team Members  | SID/GUID |
| ------------- | ------------- |
| ABRAM NIKO CERRO OBLIGACION  | 2000877 / 2609719O  |
| ABDUL HADY BIN ZAYDIE  | 2001054 / 2609734B  |


## Install requirements

Install requirements by executing the command below
```
pip3 install -r requirements.txt
```

## Building pb2 files

To build the pb2 files, run the following commands
```
cd grpc-services
python -m grpc_tools.protoc -I ../protos --python_out=. --grpc_python_out=. ../protos/tracetogether.proto
```

## Starting the server

The gRPC SafeEntry server can be started by executing the following command
```
python server.py
```

## Starting the client

The client can be started by executing the following command
```
python client.py
```
