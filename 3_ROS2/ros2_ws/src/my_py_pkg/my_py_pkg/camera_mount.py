import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import StaticTransformBroadcaster


class CameraMount(Node):
    def __init__(self):
        super().__init__('camera_mount')
        self.broadcaster = StaticTransformBroadcaster(self)   # /tf_static 으로 보내는 publisher

        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'base_link'        # 부모: 로봇 몸
        t.child_frame_id = 'camera_link'       # 자식: 카메라 (1단계와 같은 철자)
        t.transform.translation.x = 0.2        # 몸 중심에서 앞으로 0.2m
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.1        # 위로 0.1m
        t.transform.rotation.w = 1.0           # 회전 없음
        self.broadcaster.sendTransform(t)      # 처음 한 번만 보낸다


def main():
    rclpy.init()
    node = CameraMount()
    rclpy.spin(node)        # 할 일은 없지만 팻말을 들고 서 있으려고 살려 둔다
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()