import time
import grpc
from onnxGrpcServer_pb2 import Features
from onnxGrpcServer_pb2_grpc import CTCVInferenceServicerStub

from locust import task, User
from locust.exception import LocustError
from locust.user.task import LOCUST_STATE_STOPPING
import grpc.experimental.gevent as grpc_gevent

from input_data import test_data

grpc_gevent.init_gevent()


class GrpcClient(object):
    def __init__(self, environment, stub):
        self.env = environment
        self._stub_class = stub.__class__
        self._stub = stub

    def __getattr__(self, name):
        func = self._stub_class.__getattribute__(self._stub, name)

        def wrapper(*args, **kwargs):
            request_meta = {
                "request_type": "grpc",
                "name": name,
                "start_time": time.time(),
                "response_length": 0,
                "exception": None,
                "context": {},
                "response": None,
            }
            start_perf_counter = time.perf_counter()
            try:
                request_meta["response"] = func(*args, **kwargs)
                # request_meta["response_length"] = len(list(request_meta["response"]))

                # # can confirm get response data below
                # print("response:", ",".join([str(res) for res in request_meta["response"]]))
            except grpc.RpcError as e:
                request_meta["exception"] = e
            request_meta["response_time"] = (time.perf_counter() - start_perf_counter) * 1000
            self.env.events.request.fire(**request_meta)
            return request_meta["response"]

        return wrapper


class GrpcUser(User):
    abstract = True
    stub_class = None

    def __init__(self, environment):
        super().__init__(environment)
        for attr_value, attr_name in ((self.host, "host"), (self.stub_class, "stub_class")):
            if attr_value is None:
                raise LocustError(f"You must specify the {attr_name}.")
        self._channel = grpc.insecure_channel(self.host)
        self._channel_closed = False
        stub = self.stub_class(self._channel)
        self.client = GrpcClient(environment, stub)

    def stop(self, force=False):
        self._channel_closed = True
        time.sleep(1)
        self._channel.close()
        super().stop(force=True)


class TestGrpcUser(GrpcUser):
    host = "api:50051"
    stub_class = CTCVInferenceServicerStub

    @task
    def Predict(self):
        if not self._channel_closed:
            payloads = []
            for i in range(len(test_data)):
                payloads.append(Features(**test_data[i]))
            self.client.Predict(iter(payloads))