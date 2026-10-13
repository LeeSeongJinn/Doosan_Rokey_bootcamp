import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult  # 1. 누락된 임포트 추가

class ParamDemo(Node):
    def __init__(self):
        super().__init__("param_demo")
        # speed, robot_name 키의 param 생성
        self.declare_parameter("speed", 1.0)
        self.declare_parameter("robot_name", "alpha")
        self.create_timer(1.0, self.tick)  # 1초마다 self.tick 함수 호출
        self.add_on_set_parameters_callback(self.on_set)

    def tick(self):
        speed = self.get_parameter('speed').value
        robot_name = self.get_parameter('robot_name').value
        # 2. 로봇 이름과 속도 순서에 맞게 변수 매핑 수정
        self.get_logger().info("로봇이름: {} ===== 속도: {}".format(robot_name, speed))

    def on_set(self, params):
        for p in params:
            if p.name == "speed" and p.value < 0:
                return SetParametersResult(successful=False, reason="속도는 양수여야 함")
        return SetParametersResult(successful=True)


def main():
    rclpy.init()
    node = ParamDemo()
    try:
        rclpy.spin(node)
    except Exception:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()