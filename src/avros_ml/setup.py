# setup.py - build recipe for avros_ml.
#   * packages: installs both Python packages in this folder, avros_ml (the nodes) and
#     ML_Models (the PyTorch models), as long as each has an __init__.py.
#   * data_files: copies the launch files so `ros2 launch avros_ml ...` can find them.
#   * entry_points: the commands behind `ros2 run avros_ml <name>`; add a line per node.

from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'avros_ml'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='op',
    maintainer_email='yfreeman102804@gmail.com',
    description='RGB-T fusion, YOLO detection, TCN imitation learning and a safety arbiter.',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'rgbt_fusion_node = avros_ml.rgbt_fusion_node:main',
            'detector_node = avros_ml.detector_node:main',
            'il_node = avros_ml.il_node:main',
            'arbiter_node = avros_ml.arbiter_node:main',
        ],
    },
)
