from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="demogpt",
    version="1.1.1.7",
    url="https://github.com/melih-unsal/DemoGPT",
    author="Melih Unsal",
    author_email="melih@demogpt.io",
    description="Auto Gen-AI App Generator with the Power of Llama 2",
    long_description=long_description,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["streamlit", "altair<5", "langchain", "openai", "python-dotenv"],
    package_data={"prompt_based": ["prompts.txt"]},
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
    python_requires=">=3.7",
)
