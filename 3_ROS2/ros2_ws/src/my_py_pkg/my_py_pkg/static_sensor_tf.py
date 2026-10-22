import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from tf2_ros import StaticTransformBroadcaster
from geometry_msgs.msg import TransformStamped


class StaticSensorTf(Node):
    def __init__(self):
        super().__init__('static_sensor_tf')
        self._br = StaticTransformBroadcaster(self)
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'        # 부모 좌표계
        t.child_frame_id = 'sensor'            # 자식 좌표계
        t.transform.translation.x = 1.0        # x로 1m 앞
        t.transform.rotation.w = 1.0           # 회전 없음(단위 쿼터니언)
        self._br.sendTransform(t)
        self.get_logger().info('static TF 발행: base_link -> sensor')


def main():
    rclpy.init()
    node = StaticSensorTf()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()