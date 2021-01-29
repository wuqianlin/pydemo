# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import square_pb2 as square__pb2


class SquareServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.streamrangeSquare = channel.stream_stream(
        '/squarerpc_service.SquareService/streamrangeSquare',
        request_serializer=square__pb2.Message.SerializeToString,
        response_deserializer=square__pb2.Message.FromString,
        )


class SquareServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def streamrangeSquare(self, request_iterator, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SquareServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'streamrangeSquare': grpc.stream_stream_rpc_method_handler(
          servicer.streamrangeSquare,
          request_deserializer=square__pb2.Message.FromString,
          response_serializer=square__pb2.Message.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'squarerpc_service.SquareService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
