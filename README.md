# m2cgen

[![Build Status](https://travis-ci.org/BayesWitnesses/m2cgen.svg?branch=master)](https://travis-ci.org/BayesWitnesses/m2cgen)
[![Coverage Status](https://coveralls.io/repos/github/BayesWitnesses/m2cgen/badge.svg?branch=master)](https://coveralls.io/github/BayesWitnesses/m2cgen?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

m2cgen (Model 2 Code Generator) is a lightweight library which provides an easy way to transpile trained sklearn models to native code (Python, C, Java).

## Supported languages

- Python
- Java
- C (almost)

## Supported models

### Linear Regressors
- LinearRegression
- HuberRegressor
- ElasticNet
- ElasticNetCV
- TheilSenRegressor
- Lars
- LarsCV
- Lasso
- LassoCV
- LassoLars
- LassoLarsIC
- OrthogonalMatchingPursuit
- OrthogonalMatchingPursuitCV
- Ridge
- RidgeCV
- BayesianRidge
- ARDRegression
- SGDRegressor
- PassiveAggressiveRegressor

### Logistic Regressors
- LogisticRegression
- LogisticRegressionCV
- RidgeClassifier
- RidgeClassifierCV
- SGDClassifier
- PassiveAggressiveClassifier

### Decision trees
- DecisionTreeClassifier
- DecisionTreeRegressor
- ExtraTreeClassifier
- ExtraTreeRegressor

### Ensembles
- RandomForestClassifier
- ExtraTreesClassifier
- RandomForestRegressor
- ExtraTreesRegressor

## Installation

```
pip install m2cgen
```

## Usage

Here's the simple example how to transpile linear regression model to Java
```python
from sklearn.datasets import load_boston
from sklearn import linear_model
from m2cgen.exporters import export_to_java

boston = load_boston()
X, y = boston.data, boston.target

estimator = linear_model.LinearRegression()
estimator.fit(X, y)

code = export_to_java(estimator)
```

The example of the generated code:
```java
public class Model {

    public static double score(double[] input) {
        return (((((((((((((36.45948838508965) + ((input[0]) * (-0.10801135783679647))) + ((input[1]) * (0.04642045836688297))) + ((input[2]) * (0.020558626367073608))) + ((input[3]) * (2.6867338193449406))) + ((input[4]) * (-17.76661122830004))) + ((input[5]) * (3.8098652068092163))) + ((input[6]) * (0.0006922246403454562))) + ((input[7]) * (-1.475566845600257))) + ((input[8]) * (0.30604947898516943))) + ((input[9]) * (-0.012334593916574394))) + ((input[10]) * (-0.9527472317072884))) + ((input[11]) * (0.009311683273794044))) + ((input[12]) * (-0.5247583778554867));
    }
}
```
