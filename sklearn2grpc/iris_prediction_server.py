import grpc
from concurrent import futures
import time
import joblib
import iris_demo_pb2
import iris_demo_pb2_grpc
from sklearn.ensemble import RandomForestClassifier


class IrisPredictor(iris_demo_pb2_grpc.IrisPredictorServicer):

    @classmethod
    def get_trained_model(cls):
        cls._model = joblib.load('IrisClassifier.pkl')
        return cls._model

    def predict_iris_species(self, request, context):
        model = self.__class__.get_trained_model()
        sepal_length = request.sepal_length
        sepal_width = request.sepal_width
        petal_length = request.petal_length
        petal_width = request.petal_width
        result = model.predict(
            [[sepal_length, sepal_width, petal_length, petal_width]])
        response = iris_demo_pb2.IrisPredictResponse(species=result[0])
        return response  # not sure


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    iris_demo_pb2_grpc.add_IrisPredictorServicer_to_server(
        IrisPredictor(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    print("grpc server start...")
    print("Listening on port 50055")
    server.wait_for_termination()


if __name__ == '__main__':
    run()