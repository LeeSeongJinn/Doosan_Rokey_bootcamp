import rclpy
from example_interfaces.srv import AddTwoInts
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class AddClient(Node):

  def __init__(self):
    super().__init__('add_client')
    self.cli = self.create_client(AddTwoInts, 'add_two_ints')
    
    # 서버 접속 확인
    #####################################################
    while not self.cli.wait_for_service(timeout_sec=1.0):
      self.get_logger().info("서버 접속 시도 중...")
    #####################################################

  def send(self, a, b):
    req = AddTwoInts.Request()
    req.a = a
    req.b = b
    #####################################################
    future = self.cli.call_async(req)
    # 📌 응답이 올 때까지 확실히 기다리도록 인자 추가
    rclpy.spin_until_future_complete(self, future)
    return future.result()
    #####################################################

def main():
  rclpy.init()
  node = AddClient()
  
  ret = node.send(100, 200)
  
  if ret is not None:
    node.get_logger().info(f'결과 수신 성공: 100 + 200 = {ret.sum}')
  else:
    node.get_logger().error('서버 응답을 받지 못했습니다.')
    
  node.destroy_node()
  rclpy.try_shutdown()


if __name__ == '__main__':
  main()