import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String


class RcSubscriber(Node):
    def __init__(self):
        super().__init__('rc_subscriber')
        # /chatter 토픽 구독
        self.create_subscription(String, 'chatter', self.cb, 10)

    def cb(self, msg):
        # 수신한 고도 메시지 출력
        self.get_logger().info("수신함:" + msg.data)


def main():
    rclpy.init()
    node=RcSubscriber()
    try:
        rclpy.spin(node) # 노드 항시 대기
    except(KeyboardInterrupt, ExternalShutdownException):
        #종료시 처리 내용
        pass

    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__=="__main__":
    main()
