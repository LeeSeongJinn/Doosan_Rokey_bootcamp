import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from my_interfaces.action import PlayRound
from rclpy.executors import ExternalShutdownException
from rclpy.action import ActionServer
from my_interfaces.srv import RoundGuess
import time
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

class RoundNode(Node):
    def __init__(self):
        super().__init__("game_node_action")
        self.answer = "dummy"
        self.found = set()
        self.last_letter = ""
        self.pre_letter = ""
        self.last_board = ""        
        self.done = False
        self.group = ReentrantCallbackGroup()
        ActionServer(self, PlayRound, "play_round", self.execute_callback, callback_group=self.group)
        self.create_service(RoundGuess, "guess_letter", self.on_guess, callback_group=self.group)

    def on_guess(self, req, res):
        # 문자를 받고 -> 정답 확인
        letter = req.letter.strip().lower()
        self.last_letter = letter
        # res 구성 목적
        if len(letter)!=1:
            self.get_logger().info("한 글자만 들어와야 합니다")
            res.correct=False            
            res.board = "한 글자만 들어와야 합니다"#결과??? -> 1) 한 글자만 들어와야 합니다 2) 기존 board 전달?
            return res
        if letter in self.answer:
            self.found.add(letter)
            self.get_logger().info(f"정답 : {letter}")
            res.correct=True
            self.last_board = " ".join(ch if ch in self.found else "_" for ch in self.answer)
            res.board = self.last_board
            self.done = all(ch in self.found for ch in self.answer)
            res.done = self.done
            return res
        else:
            self.get_logger().info(f"오답 : {letter}")
            res.correct=False
            res.board = " ".join(ch if ch in self.found else "_" for ch in self.answer)
            return res

    def execute_callback(self, goal_handle):
        self.answer = goal_handle.request.word    
        tries = 0
        fb = PlayRound.Feedback()
        self.get_logger().info("======이제 정답을 맞춰보세요!!==========")
        # 새로 들어온 문자를 감지하고, 변화된 board 상황을 피드백 한다
        while not self.done:
            # 기존 문자, 새로운 문자 확인 ->문자와 board 만들고 피드백
            if self.pre_letter != self.last_letter:
                # 피드백을 전달하기 ( 현재들어온 문자, board )
                fb.letter = self.last_letter
                fb.board_progress = self.last_board
                goal_handle.publish_feedback(fb)
                tries +=1
            else: # 두 문자가 같을때는 피드백 전달 X
                pass 
            self.pre_letter = self.last_letter
            # fb.letter = self.last_letter
            # fb.board_progress = self.last_board
            # goal_handle.publish_feedback(fb)
            time.sleep(1)
        goal_handle.succeed()
        result = PlayRound.Result()
        result.board_result = self.last_board
        result.done = self.done
        result.tries = tries
        return result

def main():
    rclpy.init()
    node = RoundNode()
    try:
        ex = MultiThreadedExecutor()
        ex.add_node(node)
        ex.spin()
    except (ExternalShutdownException, KeyboardInterrupt) as e:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

if __name__=="__main__":
    main()