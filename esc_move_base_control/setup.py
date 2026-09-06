from setuptools import find_packages, setup

package_name = "esc_move_base_control"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        # PATCH (isaac-social-nav): install YAML so ROS 2 launch can load params
        # from share (ROS 1 launch used $(find …)/config).
        ("share/" + package_name + "/config", ["config/esc_move_base_control.yaml"]),
        ("share/" + package_name + "/launch", ["launch/esc_move_base_control.launch"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="sasm",
    maintainer_email="sasilva1998@gmail.com",
    description="TODO: Package description",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "base_controller = esc_move_base_control.base_controller:main"
        ],
    },
)
