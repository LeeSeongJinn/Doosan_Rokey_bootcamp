import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String


class MySubscriber(Node):
    def __init__(self):
        super().__init__('my_subscriber')
        
        self.create_subscription(String,'chatter',self.cb,10)
        #subsciption을 사용해서 메시지를 받는데 형식은 Stfing, 토픽 이름은 chatter, 콜백은 self.cb, qos는 10으로 한다.
        
    def cb(self,msg):
        #전달된 메세지 출력
        #수신함+msg ->logger로 출력
        self.get_logger().info("수신함:"+msg.data)

def main():
    rclpy.init()
    node=MySubscriber()
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