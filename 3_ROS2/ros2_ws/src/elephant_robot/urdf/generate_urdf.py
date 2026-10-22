#!/usr/bin/env python3
"""Regenerate the pre-expanded plain URDF from the xacro source of truth.

Usage:
    python3 src/elephant_robot/urdf/generate_urdf.py

The package ships both files:

  * ``elephant_robot.urdf.xacro`` - parameterized source, edit this one
  * ``elephant_robot.urdf``       - plain URDF used when xacro is not
                                     installed (e.g. plain robot_state_publisher)
"""

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'elephant_robot.urdf.xacro')
DST = os.path.join(HERE, 'elephant_robot.urdf')

HEADER = """<?xml version="1.0"?>
<!--
  GENERATED FILE - do not edit by hand.
  Source: elephant_robot.urdf.xacro   (regenerate with generate_urdf.py)
-->
"""


def expand():
    """Run xacro on the source file and return the expanded XML text."""
    # 1. the "xacro" console script (ros-jazzy-xacro)
    exe = shutil.which('xacro')
    if exe:
        cmd = [exe, SRC]
    else:
        # 2. "ros2 run xacro xacro"
        ros2 = shutil.which('ros2')
        if ros2:
            cmd = [ros2, 'run', 'xacro', 'xacro', SRC]
        else:
            # 3. plain python module
            try:
                import xacro
            except ImportError:
                sys.exit(
                    'error: xacro is not installed.\n'
                    '  sudo apt install ros-$ROS_DISTRO-xacro\n'
                    'or set PYTHONPATH to an xacro source checkout.')
            return xacro.process_file(SRC).toprettyxml(indent='  ')

    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
    return out


def main():
    text = expand()
    # strip the declaration xacro adds, we write our own header instead
    if text.startswith('<?xml'):
        text = text.split('?>', 1)[1].lstrip('\n')
    with open(DST, 'w') as fh:
        fh.write(HEADER + text)
    print('wrote %s (%d bytes)' % (DST, os.path.getsize(DST)))


if __name__ == '__main__':
    main()
