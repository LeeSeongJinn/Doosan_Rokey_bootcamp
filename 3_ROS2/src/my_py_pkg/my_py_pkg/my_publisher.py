import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String


class MyPublisher(Node):
    def __init__(self):
        super().__init__('my_publisher')
        self.num=1        
        #pub
        self.pub=self.create_publisher(String, 'chatter', 10) #메세지 타입, 토픽명, QoS 설정
        #일정 시간마다 실행 -> timer
        self.create_timer(1.0, self.tick) #몇 초마다, 어떤 콜백함수를 호출할 건지

    def tick(self):
        #1. 전달할 메세지 만들기
        #   - Hello Ros: 1
        #   - log
        #2. pub를 이용해 송출하기(pub 변수 활용)
        msg=String()
        msg.data=f"Hello ROS:{self.num}"
        self.get_logger().info(f"발행:'{msg.data}'")
        self.pub.publish(msg)
        self.num+=1
        pass

def main():
    rclpy.init()
    node=MyPublisher()
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