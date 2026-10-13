import rclpy
from my_interface.srv import Calc
from rclpy.node import Node


class CalcServer(Node):

  def __init__(self):
    super().__init__('calc_server')
    self.create_service(Calc, 'calc', self.on_request)
    self.get_logger().info('=====계산기 대기중=====')

  def on_request(self, req, res):
    # req가 a, b, op 담아서 보냄
    # op가 무엇인지에 따라 (+-*/) 계산이 이루어지고, 응답값이 만들어진다
    a = req.a
    b = req.b
    op = req.op

    if op == '+':
      res.result = float(a + b)
      res.ok = True
    elif op == '-':
      res.result = float(a - b)
      res.ok = True
    elif op == '*':
      res.result = float(a * b)
      res.ok = True
    elif op == '/':
      if b != 0:
        res.result = float(a / b)
        res.ok = True
      else:
        res.result = 0.0
        res.ok = False  # 0으로 나누는 경우
    else:
      res.result = 0.0
      res.ok = False  # 잘못된 연산자

    # 로그 출력
    self.get_logger().info(
        f'요청 받음: {a} {op} {b} => 결과: {res.result}, 성공여부: {res.ok}'
    )
    return res


def main():
  rclpy.init()
  node = CalcServer()
  try:
    rclpy.spin(node)  # 노드 항시 대기
  except Exception:
    pass
  finally:
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
  main()