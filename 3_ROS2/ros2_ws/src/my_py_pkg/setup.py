import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'my_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lsj',
    maintainer_email='lsj@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'my_publisher=my_py_pkg.my_publisher:main',
            'my_subscriber=my_py_pkg.my_subscriber:main',
            'add_server=my_py_pkg.add_server:main',
            'add_client=my_py_pkg.add_client:main',
            'executor_demo=my_py_pkg.executor_demo:main',
            'count_up_server=my_py_pkg.count_up_server:main',
            'count_up_client=my_py_pkg.count_up_client:main',
            'calc_server=my_py_pkg.calc_server:main',
            'argument=my_py_pkg.argument:main',
            'calculator=my_py_pkg.calculator:main'

        ],
    },
)
