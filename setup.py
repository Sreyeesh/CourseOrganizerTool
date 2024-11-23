from setuptools import setup, find_packages

setup(
    name="course-organizer",
    version="1.0.0",
    author="Sreyeesh Garimella",
    author_email="sgarime1@gmail.com",
    description="A CLI tool to organize Udemy courses and videos",
    packages=find_packages(),
    install_requires=[
        "click",
        "tqdm"
    ],
   entry_points={
    "console_scripts": [
        "course-organizer=course_organizer.organizer:cli",
    ],
},

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
