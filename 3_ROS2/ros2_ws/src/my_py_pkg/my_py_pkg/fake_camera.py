import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped


class FakeCamera(Node):
    def __init__(self):
        super().__init__('fake_camera')
        self.pub = self.create_publisher(PointStamped, 'cup_in_camera', 10)
        self.timer = self.create_timer(0.5, self.tick)   # 0.5초마다 "봤다"

    def tick(self):
        msg = PointStamped()
        msg.header.frame_id = 'camera_link'                  # 누구 기준인지 이름표
        msg.header.stamp = self.get_clock().now().to_msg()   # 언제 봤는지
        msg.point.x = 1.0                                    # 카메라 눈에서 앞으로 1m
        msg.point.y = 0.3                                    # 왼쪽으로 0.3m
        msg.point.z = 0.0
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = FakeCamera()
    rclpy.spin(node)        # 여기서 멈춰 서서 0.5초마다 tick 을 부른다
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()