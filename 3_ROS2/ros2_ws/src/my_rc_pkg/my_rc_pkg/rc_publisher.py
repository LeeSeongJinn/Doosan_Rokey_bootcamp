import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String


class RcPublisher(Node):
    def __init__(self):
        super().__init__('rc_publisher')
        self.num=1        
        #pub
        self.pub=self.create_publisher(String, 'chatter', 10) #메세지 타입, 토픽명, QoS 설정
        #일정 시간마다 실행 -> timer
        self.create_timer(0.3, self.tick) #몇 초마다, 어떤 콜백함수를 호출할 건지

    def tick(self):
        # 1. 메시지 생성 및 발행
        msg = String()
        msg.data = f"Rocket Height:{self.num}"
        self.get_logger().info(f"발행:'{msg.data}'")
        self.pub.publish(msg)

        # 2. 100m 돌파 여부 확인 (self.num 변수 활용)
        if self.num > 0 and self.num % 100 == 0:
            stage = self.num // 100
            self.get_logger().info(
                f"🚀 {self.num}m 돌파! {stage}번 로켓 분리!"
            )

        # 3. 카운트 증가
        self.num += 1

def main():
    rclpy.init()
    node=RcPublisher()
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