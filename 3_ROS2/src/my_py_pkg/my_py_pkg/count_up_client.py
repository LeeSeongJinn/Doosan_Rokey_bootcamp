import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from my_interface.action import CountUp

class CountUpClient(Node):
    def __init__(self):
        super().__init__("count_up_client")
        self.cli = ActionClient(self, CountUp, "count_up")

    def send(self, target):
        #interface에 맟춰서 메시지 구성-> 서버 확인-> goal 전송-> "응답을 대기(승인?)"
        goal=CountUp.Goal()
        goal.target=target
        self.cli.wait_for_server()
        fut=self.cli.send_goal_async(goal, feedback_callback=self.on_fb)
        fut.add_done_callback(self.on_accept)

    def on_accept(self,fut):
        gh=fut.result()
        if gh.accepted:
            gh.get_result_async().add_done_callback(self.on_result)
        else:
            self.get_logger().error("요청 거절")
            return

    def on_result(self,fut):
        self.get_logger().warn(f"작업 완료: {fut.result().result.sequence}")
        rclpy.try_shutdown()
    

    def on_fb(self, msg):
        self.get_logger().info(f"현재 피드백: {msg.feedback.current}")


def main():
    rclpy.init()
    node=CountUpClient()
    node.send(target=3)
    try:
        rclpy.spin(node)
    except Exception:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__=="__main__":
    main()

