import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class QosListener(Node):
    def __init__(self):
        super().__init__("qos_listener")
        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT, history=HistoryPolicy.KEEP_LAST, depth=10)
        #qos = QoSProfile(reliability=ReliabilityPolicy.RELIABLE, history=HistoryPolicy.KEEP_LAST, depth=10)
        self.create_subscription(String,"qos_chat",self.on_msg,qos_profile=qos)

    def on_msg(self, msg):
        self.get_logger().info(f"받은 메시지 ====> {msg.data}")

def main():
    rclpy.init()
    node = QosListener()
    try:
        rclpy.spin(node)
    except Exception:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__=="__main__":
    main()