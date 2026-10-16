cmake_minimum_required(VERSION 3.8)
project(my_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Mission.msg"
  "srv/AddThreeInts.srv"
  "srv/TurtleGoal.srv"
  "action/CountUp.action"
  "srv/Calc.srv"
  "action/ArithmeticChecker.action"
  "msg/ArithmeticArgument.msg"
  "srv/ArithmeticOperator.srv"
  "action/PlayRound.action"
  "srv/RoundGuess.srv"
  "action/PatrolAction.action"
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
