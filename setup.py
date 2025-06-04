from setuptools import setup, find_packages

setup(
    name="vt_dlhub",
    version="1.1.5",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    author="vantu03",
    description="TikTok downloader library by VT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vantu03/vt_dlhub",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
