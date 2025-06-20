#!/usr/bin/env python3
"""Setup script for Hassaniya Text Normalizer."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            requirements.append(line)

setup(
    name="hassaniya-normalizer",
    version="0.1.0",
    author="Hassaniya Normalizer Team",
    author_email="",
    description="A production-ready Python package for normalizing Hassaniya Arabic text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hassaniya-normalizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Natural Language :: Arabic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": ["pytest>=8.2", "ruff>=0.4.1"],
        "web": ["gradio>=4.0.0", "flask>=2.0.0", "flask-cors>=4.0.0"],
    },
    entry_points={
        "console_scripts": [
            "hassaniya-normalize=cli.normalize_text:main",
            "hassaniya-web=web_ui.server:main",
            "hassaniya-gradio=app.gradio_ui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "normalizer": ["../data/*.json", "../data/*.jsonl"],
        "": ["data/*.json", "data/*.jsonl"],
    },
    zip_safe=False,
)