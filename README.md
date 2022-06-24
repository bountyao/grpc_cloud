# grpc_cloud
cd grpc-services

## Build pb2 files
python -m grpc_tools.protoc -I ../protos --python_out=. --grpc_python_out=. ../protos/tracetogether.proto

## Install Requirements
pip3 install -r requirements.txt

## Start server
python server.py

## Start client
python client.py