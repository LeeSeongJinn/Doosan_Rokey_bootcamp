import rclpy
from example_interfaces.srv import AddTwoInts
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class AddServer(Node):

  def __init__(self):
    super().__init__('add_server')

    # 서비스 서버 생성
    self.create_service(AddTwoInts, 'add_two_ints', self.on_request)
    
  def on_request(self, req, res):
    sum_val = req.a + req.b
    res.sum = sum_val

    # self.get_logger() 괄호 추가 및 {res.sum}으로 수정
    self.get_logger().info(
        f'두 수 {req.a}와 {req.b}의 합은 {res.sum}입니다'
    )
    return res


def main():
  rclpy.init()
  node = AddServer()
  try:
    rclpy.spin(node)  # 노드 항시 대기
  except (KeyboardInterrupt, ExternalShutdownException):
    pass
  finally:
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
  main()