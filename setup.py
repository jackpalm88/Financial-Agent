"""
Financial Agent - Setup Configuration
Tool-Augmented Multi-Modal Trading System
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file) as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="financial-agent",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Tool-Augmented Multi-Modal Trading System with INoT Architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/financial-agent",
    
    # Package discovery
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Python version requirement
    python_requires=">=3.9",
    
    # Dependencies
    install_requires=requirements,
    
    # Optional dependencies
    extras_require={
        "dev": [
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
            "isort>=5.12.0",
            "ipython>=8.14.0",
        ],
        "test": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.1",
        ],
        "monitoring": [
            "prometheus-client>=0.17.0",
            "sentry-sdk>=1.28.0",
        ],
    },
    
    # Entry points (CLI commands)
    entry_points={
        "console_scripts": [
            "financial-agent=financial_agent.cli:main",
        ],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial :: Investment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    
    # Keywords
    keywords="trading, finance, ai, llm, mt5, metatrader, algorithmic-trading",
    
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/yourusername/financial-agent/issues",
        "Source": "https://github.com/yourusername/financial-agent",
        "Documentation": "https://github.com/yourusername/financial-agent/wiki",
    },
)
