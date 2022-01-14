#!/usr/bin/python

from setuptools import setup

setup(
    name='aac',
    version='0.1.0',
    install_requires=[
        'fire',
        'mediapipe',
        'numpy',
        'opencv-python',
        'toml'
    ],
    entry_points={
        'console_scripts': [
            "aac = core.main:main"
        ]
    }
)