from setuptools import setup, find_packages

setup(
    name="tokintel",
    version="2.0.0",
    description="TokIntel v2 – AI-powered TikTok Analyzer",
    author="Matteo Papetti",
    license="MIT",
    packages=find_packages(where="TokIntel_v2"),
    package_dir={"": "TokIntel_v2"},
    include_package_data=True,
    install_requires=[
        "streamlit",
        "pandas",
        "scikit-learn",
        "plotly",
        "easyocr",
        "openai",
        "torch",
        "transformers",
    ],
    entry_points={
        "console_scripts": [
            "tokintel-launch=ui.streamlit_launcher:main",
        ],
    },
    python_requires=">=3.9",
) 