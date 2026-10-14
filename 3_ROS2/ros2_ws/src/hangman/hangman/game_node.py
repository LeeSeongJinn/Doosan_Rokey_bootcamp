import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class GameNode(Node):
    def __init__(self):
        super().__init__("game_node")
        # 정답을 미리 세팅
        self.answer="rok"
        # 게임이 진행되는 동안 들어왔던 추측값들 종합
        self.found= set() #r _ _ _ _ 
        # sub: 추측값 받기, pub: 게임 진행상황 송출
        self.create_subscription(String, "guess", self.on_guess, 10)
        self.pub=self.create_publisher(String, "board",10)

    def on_guess(self, msg):
        # letter를 전달받고-> answer 내용에 매칭 -> 맞으면 found에 등록 -> 틀리면 넘기기 
        # 이후에 송출부분 작성
        letter=msg.data.strip().lower() # 공백 제거와 소문자 처리 필요
        if len(letter)!=1: # 한 글자만 받기
            self.get_logger().info("한 글자만 들어와야 합니다.")
            return

        if letter in self.answer:
            self.found.add(letter)
            self.get_logger().info(f"정답 : {letter}")
        else:
            self.get_logger().info(f"오답 : {letter}")

        #publisher : msg 구성-> 값을 채우고(r _ _ _ _) -> 송출
        done, board=self.check_board()
        board_msg=String()
        board_msg.data=board
        self.pub.publish(board_msg)
        # 완료 : answer의 모든 문자가 found에 있으면 다 찾은 것!
        if done:
            self.get_logger().info("승리 단어 완성")
        
    def check_board(self):
        done=all(ch in self.found for ch in self.answer)
        board=" ".join(ch if ch in self.found else "_" for ch in self.answer)
        return done, board
    


def main():
    rclpy.init()
    node=GameNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("종료합니다.")
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__=="__main__":
    main()