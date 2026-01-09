"""
Setup configuration for 27z-6 Role Evaluator.

This allows the package to be installed in development mode:
    pip install -e .

Or as a regular package:
    pip install .
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README for the long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="27z-6-role-evaluator",
    version="1.0.0",
    description="Layoff notice aggregation, risk assessment, and visualization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",  # TODO: Update with your name
    author_email="your.email@example.com",  # TODO: Update with your email
    url="https://github.com/chromaglow/27z-6_role_evaluator",
    license="MIT",
    
    # Package discovery
    packages=find_packages(exclude=["tests", "tests.*", "docs", "scripts"]),
    
    # Include non-Python files
    include_package_data=True,
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=[
        "pdfplumber>=0.10.0,<0.11.0",
        "geopy>=2.4.0,<3.0.0",
    ],
    
    # Optional dependencies for development
    extras_require={
        "dev": [
            "pytest>=7.4.0,<8.0.0",
            "pytest-cov>=4.1.0,<5.0.0",
            "black>=23.0.0,<24.0.0",
            "flake8>=6.1.0,<7.0.0",
            "mypy>=1.7.0,<2.0.0",
            "isort>=5.12.0,<6.0.0",
        ],
    },
    
    # Entry points for CLI commands
    entry_points={
        "console_scripts": [
            "risk-assessment=tools.risk_assessment:main",
        ],
    },
    
    # Classifiers for PyPI (if you ever publish)
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
