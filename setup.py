"""Setup script for NEXUS"""

from setuptools import setup, find_packages

setup(
    name="nexus-ai",
    version="0.1.0",
    description="Self-Evolving Coding Intelligence",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.0",
        "pydantic>=2.0.0",
        "rich>=13.0.0",
        "google-generativeai>=0.3.0",
        "anthropic>=0.18.0",
        "aiohttp>=3.9.0",
    ],
    entry_points={
        "console_scripts": [
            "nexus=nexus.__main__:main",
        ],
    },
    python_requires=">=3.9",
)
