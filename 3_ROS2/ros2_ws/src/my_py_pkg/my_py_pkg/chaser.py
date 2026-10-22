import math

import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from geometry_msgs.msg import PointStamped, Twist
from tf2_ros import Buffer, TransformListener
import tf2_geometry_msgs  # noqa: F401  불러오기만 해도 PointStamped 바꾸는 법이 등록된다


class Chaser(Node):
    def __init__(self):
        super().__init__('chaser')
        # 3단계: 나무를 쌓아 둘 Buffer와, /tf · /tf_static 을 받는 Listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        # 카메라 소식을 받는 subscriber
        self.sub = self.create_subscription(
            PointStamped, 'cup_in_camera', self.on_cup, 10)
        # 4단계: 바퀴에게 명령을 보내는 publisher
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)

    def on_cup(self, msg):
        # 3단계: 카메라 기준을 몸 기준으로 바꾼다
        try:
            cup_in_base = self.tf_buffer.transform(
                msg, 'base_link', timeout=Duration(seconds=0.1))
        except Exception as e:
            self.get_logger().warn(f'아직 바꿀 수 없음: {e}')
            return
        x = cup_in_base.point.x
        y = cup_in_base.point.y
        self.get_logger().info(f'몸 기준 컵: x={x:.2f}, y={y:.2f}')

        # 4단계: 위치를 몸 전체 속도로 바꾼다
        angle = math.atan2(y, x)       # 컵이 몸 정면에서 얼마나 옆에 있나
        dist = math.hypot(x, y)        # 컵까지 몇 미터인가

        cmd = Twist()
        if dist < 0.3:                 # 충분히 가까우면 멈춘다
            pass                       # 빈 Twist = 모두 0 = 정지
        else:
            cmd.angular.z = 1.0 * angle              # 옆에 있을수록 빨리 돈다
            if abs(angle) < 0.3:                     # 거의 정면일 때만
                cmd.linear.x = min(0.5 * dist, 0.3)  # 앞으로 간다 (최대 0.3 m/s)
        self.cmd_pub.publish(cmd)


def main():
    rclpy.init()
    node = Chaser()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()