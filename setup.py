from setuptools import setup, find_packages

setup(
    name="course-organizer-cli",
    version="1.0.0",
    description="A CLI tool for managing videos and course organization.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Sreyeesh Garimella",
    packages=find_packages(),  # Automatically finds all packages, including `course_organizer`
    install_requires=[
        "click",  # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "organizer=course_organizer.organizer:cli",  # Entry point for the CLI tool
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
