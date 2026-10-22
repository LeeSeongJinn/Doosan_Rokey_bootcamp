import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

WHEEL_GAP = 0.16          # 두 바퀴 사이 거리 (m)


class WheelDriver(Node):
    def __init__(self):
        super().__init__('wheel_driver')
        self.v = 0.0      # 앞으로 가는 속도
        self.w = 0.0      # 도는 속도
        self.last_cmd_time = self.get_clock().now()
        self.create_subscription(Twist, 'cmd_vel', self.on_cmd, 10)
        self.create_timer(0.1, self.drive)

    def on_cmd(self, msg):
        # 받은 명령을 적어 두기만 한다
        self.v = msg.linear.x
        self.w = msg.angular.z
        self.last_cmd_time = self.get_clock().now()

    def drive(self):
        # 바퀴는 따로 0.1초마다 돌린다
        silence = (self.get_clock().now() - self.last_cmd_time).nanoseconds / 1e9
        if silence > 0.5:                      # 0.5초 동안 소식이 없으면 멈춘다
            self.v, self.w = 0.0, 0.0
        left = self.v - self.w * WHEEL_GAP / 2
        right = self.v + self.w * WHEEL_GAP / 2
        self.get_logger().info(f'왼쪽 {left:.3f} m/s, 오른쪽 {right:.3f} m/s')


def main():
    rclpy.init()
    node = WheelDriver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()