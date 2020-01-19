from setuptools import setup


setup(
    setup_requires=["wheel >= 0.32", "pytest-runner >= 5.0, <6.0"],
    entry_points={"console_scripts": ["k8secrets = k8secrets.__main__:main"]},
)
