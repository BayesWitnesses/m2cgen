# m2cgen

[![Build Status](https://travis-ci.org/BayesWitnesses/m2cgen.svg?branch=master)](https://travis-ci.org/BayesWitnesses/m2cgen)
[![Coverage Status](https://coveralls.io/repos/github/BayesWitnesses/m2cgen/badge.svg?branch=master)](https://coveralls.io/github/BayesWitnesses/m2cgen?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**m2cgen** (Model 2 Code Generator) - is a lightweight library which provides an easy way to transpile trained statistical models into a native code (Python, C, Java).

## Supported languages

- Python
- Java
- C

## Supported models
<table>
  <thead>
      <tr>
        <th width="10%"></th>
        <th width="45%">Classification</th>
        <th width="45%">Regression</th>
      </tr>
  </thead>
  <tbody>
      <tr>
        <th>Linear</th>
        <td>LogisticRegression, LogisticRegressionCV, RidgeClassifier, RidgeClassifierCV, SGDClassifier, PassiveAggressiveClassifier</td>
        <td>LinearRegression, HuberRegressor, ElasticNet, ElasticNetCV, TheilSenRegressor, Lars, LarsCV, Lasso, LassoCV, LassoLars, LassoLarsIC, OrthogonalMatchingPursuit, OrthogonalMatchingPursuitCV, Ridge, RidgeCV, BayesianRidge, ARDRegression, SGDRegressor, PassiveAggressiveRegressor</td>
      </tr>
      <tr>
        <th>SVM</th>
        <td>LinearSVC</td>
        <td>LinearSVR</td>
      </tr>
      <tr>
        <th>Tree</th>
        <td>DecisionTreeClassifier, ExtraTreeClassifier</td>
        <td>DecisionTreeRegressor, ExtraTreeRegressor</td>
      </tr>
      <tr>
        <th>Random Forest</th>
        <td>RandomForestClassifier, ExtraTreesClassifier</td>
        <td>RandomForestRegressor, ExtraTreesRegressor</td>
      </tr>
  </tbody>
</table>

## Installation

```
pip install m2cgen
```

## Usage

Here's a simple example of how a trained linear model can be represented in Java code:
```python
from sklearn.datasets import load_boston
from sklearn import linear_model
import m2cgen as m2c

boston = load_boston()
X, y = boston.data, boston.target

estimator = linear_model.LinearRegression()
estimator.fit(X, y)

code = m2c.export_to_java(estimator)
```

The example of the generated code:
```java
public class Model {

    public static double score(double[] input) {
        return (((((((((((((36.45948838508965) + ((input[0]) * (-0.10801135783679647))) + ((input[1]) * (0.04642045836688297))) + ((input[2]) * (0.020558626367073608))) + ((input[3]) * (2.6867338193449406))) + ((input[4]) * (-17.76661122830004))) + ((input[5]) * (3.8098652068092163))) + ((input[6]) * (0.0006922246403454562))) + ((input[7]) * (-1.475566845600257))) + ((input[8]) * (0.30604947898516943))) + ((input[9]) * (-0.012334593916574394))) + ((input[10]) * (-0.9527472317072884))) + ((input[11]) * (0.009311683273794044))) + ((input[12]) * (-0.5247583778554867));
    }
}
```

TODO: explain the difference between regression (single value output) and classification (multi-value output). Show how to handle vector outputs in C.

## CLI

`m2cgen` can be used as a CLI tool to generate code using serialized model objects (pickle protocol):
```
$ m2cgen <pickle_file> --language <language> [--indent <indent>]
         [--class_name <class_name>] [--package_name <package_name>]
```

Piping is also supported:
```
$ cat <pickle_file> | m2cgen --language <language>
```
