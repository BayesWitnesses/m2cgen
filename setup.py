from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="m2cgen",
    version="0.4.1",
    url="https://github.com/BayesWitnesses/m2cgen",
    description="Code-generation for various ML models into native code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data={
        "": ["linear_algebra.java", "linear_algebra.c", "linear_algebra.go",
             "linear_algebra.js"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords="sklearn ml code-generation",
    python_requires=">=3.5",
    install_requires=[
        "numpy",
        "scipy",
        "scikit-learn",
    ],
    entry_points={
        "console_scripts": [
            "m2cgen = m2cgen.cli:main",
        ],
    }
)
