import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

class MapPub(Node):
    def __init__(self):
        super().__init__("map_pub")
        
        # 💡 테스트할 때 여기를 VOLATILE 또는 TRANSIENT_LOCAL로 바꿔가며 비교해 보세요!
        map_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,  # 혹은 DurabilityPolicy.TRANSIENT_LOCAL
            depth=10
        )
        
        self.pub = self.create_publisher(String, "map_info", map_qos)
        self.get_logger().info("MapPub 노드 대기중 ")
        
        self.count = 0
        # 1초 뒤에 한 번 발행하기 위한 타이머
        self.timer = self.create_timer(1.0, self.pub_map_info)

    def pub_map_info(self):
        self.count += 1
        current_time = self.get_clock().now().to_msg().sec
        
        msg = String()
        # 메시지마다 번호와 발행 시각을 다르게 부여하여 차이를 명확히 확인합니다.
        msg.data = f"[메시지 번호: {self.count}] 발행시각({current_time}초): ROKEY공장 정보 전송 완료!"
        
        self.pub.publish(msg)
        self.get_logger().info(f"발행된 메시지: {msg.data}")
        
        # 단 한 번만 발행하고 타이머를 끕니다.
        self.timer.cancel()


def main():
    rclpy.init()
    node = MapPub()
    try:
        rclpy.spin(node)
    except Exception:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__ == "__main__":
    main()