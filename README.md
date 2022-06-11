# grpc_cloud
cd grpc-services

## Build pb2 files
python -m grpc_tools.protoc -I ../protos --python_out=. --grpc_python_out=. ../protos/tracetogether.proto

## Start server
python server.py

## Start client
python client.py