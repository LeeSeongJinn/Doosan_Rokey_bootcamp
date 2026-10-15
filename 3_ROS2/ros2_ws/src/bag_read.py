import rosbag2_py
from rclpy.serialization import deserialize_message
from std_msgs.msg import String

# 1) Reader 객체 생성 후 같은 형식으로 열기
reader = rosbag2_py.SequentialReader()
storage_options = rosbag2_py.StorageOptions(uri='code_bag', storage_id='mcap')
converter_options = rosbag2_py.ConverterOptions(
    input_serialization_format='cdr',
    output_serialization_format='cdr')
reader.open(storage_options, converter_options)

# 2) 메시지가 남아 있는 동안 하나씩 읽기
while reader.has_next():
    topic, data, t = reader.read_next()       # (토픽명, 직렬화 바이트, 타임스탬프 ns)
    msg = deserialize_message(data, String)   # 바이트를 다시 메시지로 복원
    print(f'[{t}] {topic} -> {msg.data}')