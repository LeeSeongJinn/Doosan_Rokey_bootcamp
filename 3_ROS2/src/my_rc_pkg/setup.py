from setuptools import find_packages, setup

package_name = 'my_rc_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            'rc_publisher=my_rc_pkg.rc_publisher:main',
            'rc_subscriber=my_rc_pkg.rc_subscriber:main',
        ],
    },
)
