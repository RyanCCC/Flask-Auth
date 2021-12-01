# sklearn to grpc
1. 开始实例之，使用pip安装```grpcio```、```grpcio-tools```、```protobuf```
2. 训练一个随机森林分类模型，把训练好的模型保存为pkl文件，详情请见：```train_model.py```
3. 通过protobuf定义接口和数据类型
4. 使用gRPC protobuf生成Python的库函数
    ``` sh
    python -m grpc_tools.protoc -I .  --python_out=. --grpc_python_out=. ./iris_demo.proto
    ```
5. 编写一个服务：```iris_prediction_server.py```
6. 编写客户端：```iris_prediction_client.py```

