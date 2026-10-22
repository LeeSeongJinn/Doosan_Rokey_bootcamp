# tf_reader.py — base_link -> sensor 변환을 1초마다 조회
import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from tf2_ros import Buffer, TransformListener
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException


class TfReader(Node):
    def __init__(self):
        super().__init__('tf_reader')
        self._buffer = Buffer()
        self._listener = TransformListener(self._buffer, self)
        self.create_timer(1.0, self._lookup)

    def _lookup(self):
        try:
            tf = self._buffer.lookup_transform(
                'base_link', 'sensor', rclpy.time.Time())   # 최신 변환
            tr = tf.transform.translation
            self.get_logger().info(f'base_link->sensor = ({tr.x}, {tr.y}, {tr.z})')
        except (LookupException, ConnectivityException, ExtrapolationException) as e:
            self.get_logger().warn(f'변환 조회 실패(트리 끊김 가능): {e}')


def main():
    rclpy.init()
    node = TfReader()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()