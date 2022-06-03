from setuptools import setup, find_packages

packages=find_packages()
print(packages)
setup(
    name="icanpe-short-url",
    version="0.1.0",
    author="icanpe-dev",
    description="iCanPe Short Url",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: Private",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)