from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("m2cgen/VERSION.txt") as f:
    version = f.read().strip()

setup(
    name="m2cgen",
    version=version,
    url="https://github.com/BayesWitnesses/m2cgen",
    description="Code-generation for various ML models into native code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(exclude=["tests.*", "tests", "tools"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords="sklearn ml code-generation",
    python_requires=">=3.4",
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
