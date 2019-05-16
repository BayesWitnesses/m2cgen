from setuptools import find_packages, setup

setup(
    name="m2cgen",
    version="0.3.0",
    url="https://github.com/BayesWitnesses/m2cgen",
    description="Code-generation for various ML models into native code.",
    license="MIT",
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data={
        "": ["linear_algebra.java", "linear_algebra.c", "linear_algebra.go"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords="sklearn ml code-generation",
    python_requires="!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
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
