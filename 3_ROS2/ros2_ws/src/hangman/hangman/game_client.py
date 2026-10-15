import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class GameClient(Node):
    def __init__(self):
        super(). __init__("game_client")
        # pub, timer, 알파벳 모음 -> 콜백
        self.alphabets=list("abcdefghijklmnopqrstuy")
        self.pub=self.create_publisher(String, "guess", 10)
        self.create_timer(1, self.tick)

    def tick(self):
        #알파벳에서 문자를 하나씩 뽑아내서, 이 문자를 pub 한다
        if self.alphabets:
            letter=self.alphabets.pop(0)
            msg=String()
            msg.data=letter
            self.pub.publish(msg)
            self.get_logger().info(f"현재 들어온 알파벳: {letter}")
        else:
            self.get_logger().info("모든 알파벳 사용했습니다")
            rclpy.shutdown()
            
    


def main():
    rclpy.init()
    node=GameClient()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("종료합니다.")
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__=="__main__":
    main()