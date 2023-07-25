from setuptools import setup, find_packages

setup(
    name="demogpt",
    version="1.1.1.7",
    url="https://github.com/melih-unsal/DemoGPT",
    author="Melih Unsal",
    author_email="melih@demogpt.io",
    description="Description of my package",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "streamlit",
        "langchain",
        "openai",
        "python-dotenv"
    ],
    package_data={
    "prompt_based": ["prompts.txt"]
    },
    entry_points={
        "console_scripts": [
            "demogpt = prompt_based.cli:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
