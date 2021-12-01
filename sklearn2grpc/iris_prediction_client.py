import grpc
import iris_demo_pb2
import iris_demo_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50055')
    stub = iris_demo_pb2_grpc.IrisPredictorStub(channel)
    request = iris_demo_pb2.IrisPredictRequest(
        sepal_length=6.7,
        sepal_width=3.0,
        petal_length=5.2,
        petal_width=2.3)
    response = stub.predict_iris_species(request)
    print('The prediction is :', response.species)


if __name__ == '__main__':
    run()