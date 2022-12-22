import setuptools
from pathlib import Path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="wsapp",
    version="0.0.1",
    author="Loïc Faure-Lacroix",
    author_email="lamerstar@gmail.com",
    description="A ready to use ws app server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llacroix/overlaymodule",
    project_urls={
        "Bug Tracker": "https://github.com/llacroix/overlaymodule/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    package_data={
    },
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.4",
    install_requires=[
        # 'importlib',
    ],
    entry_points={
    }
)
