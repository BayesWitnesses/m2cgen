from setuptools import find_packages, setup

setup(
    name='m2cgen',
    version='0.1.0',
    url='https://github.com/BayesWitnesses/m2cgen',
    description='Code-generation for various ML models into native code.',
    license='MIT',
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    python_requires='!=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[
        "numpy",
        "scipy",
        "scikit-learn",
    ],
    entry_points={
        'console_scripts': [
            'gen = m2cgen.cli.gen:main',
        ],
    }
)
