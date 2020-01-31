# m2cgen

[![Build Status](https://travis-ci.org/BayesWitnesses/m2cgen.svg?branch=master)](https://travis-ci.org/BayesWitnesses/m2cgen)
[![Coverage Status](https://coveralls.io/repos/github/BayesWitnesses/m2cgen/badge.svg?branch=master)](https://coveralls.io/github/BayesWitnesses/m2cgen?branch=master)
[![License: MIT](https://img.shields.io/github/license/BayesWitnesses/m2cgen.svg)](https://github.com/BayesWitnesses/m2cgen/blob/master/LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/m2cgen.svg?logo=python&logoColor=white)](https://pypi.org/project/m2cgen)
[![PyPI Version](https://img.shields.io/pypi/v/m2cgen.svg?logo=pypi&logoColor=white)](https://pypi.org/project/m2cgen)
[![Downloads](https://pepy.tech/badge/m2cgen)](https://pepy.tech/project/m2cgen)

**m2cgen** (Model 2 Code Generator) - is a lightweight library which provides an easy way to transpile trained statistical models into a native code (Python, C, Java, Go, JavaScript, Visual Basic, C#, PowerShell, R, PHP).

* [Installation](#installation)
* [Supported Languages](#supported-languages)
* [Supported Models](#supported-models)
* [Classification Output](#classification-output)
* [Usage](#usage)
* [CLI](#cli)
* [FAQ](#faq)

## Installation
Supported Python version is >= **3.5**.
```
pip install m2cgen
```


## Supported Languages

- C
- C#
- Go
- Java
- JavaScript
- PHP
- PowerShell
- Python
- R
- Visual Basic

## Supported Models

|  | Classification | Regression |
| --- | --- | --- |
| **Linear** | <ul><li>LogisticRegression</li><li>LogisticRegressionCV</li><li>PassiveAggressiveClassifier</li><li>Perceptron</li><li>RidgeClassifier</li><li>RidgeClassifierCV</li><li>SGDClassifier</li></ul> | <ul><li>ARDRegression</li><li>BayesianRidge</li><li>ElasticNet</li><li>ElasticNetCV</li><li>HuberRegressor</li><li>Lars</li><li>LarsCV</li><li>Lasso</li><li>LassoCV</li><li>LassoLars</li><li>LassoLarsCV</li><li>LassoLarsIC</li><li>LinearRegression</li><li>OrthogonalMatchingPursuit</li><li>OrthogonalMatchingPursuitCV</li><li>PassiveAggressiveRegressor</li><li>Ridge</li><li>RidgeCV</li><li>SGDRegressor</li><li>TheilSenRegressor</li></ul> |
| **SVM** | <ul><li>LinearSVC</li><li>NuSVC</li><li>SVC</li></ul> | <ul><li>LinearSVR</li><li>NuSVR</li><li>SVR</li></ul> |
| **Tree** | <ul><li>DecisionTreeClassifier</li><li>ExtraTreeClassifier</li></ul> | <ul><li>DecisionTreeRegressor</li><li>ExtraTreeRegressor</li></ul> |
| **Random Forest** | <ul><li>ExtraTreesClassifier</li><li>LGBMClassifier(rf booster only)</li><li>RandomForestClassifier</li><li>XGBRFClassifier(binary only, multiclass is not supported yet)</li></ul> | <ul><li>ExtraTreesRegressor</li><li>LGBMRegressor(rf booster only)</li><li>RandomForestRegressor</li><li>XGBRFRegressor</li></ul> |
| **Boosting** | <ul><li>LGBMClassifier(gbdt/dart/goss booster only)</li><li>XGBClassifier(gbtree/gblinear booster only)</li><ul> | <ul><li>LGBMRegressor(gbdt/dart/goss booster only)</li><li>XGBRegressor(gbtree/gblinear booster only)</li></ul> |

## Classification Output
### Linear/Linear SVM
#### Binary
Scalar value; signed distance of the sample to the hyperplane for the second class.
#### Multiclass
Vector value; signed distance of the sample to the hyperplane per each class.
#### Comment
The output is consistent with the output of ```LinearClassifierMixin.decision_function```.

### SVM
#### Binary
Scalar value; signed distance of the sample to the hyperplane for the second class.
#### Multiclass
Vector value; one-vs-one score for each class, shape (n_samples, n_classes * (n_classes-1) / 2).
#### Comment
The output is consistent with the output of ```BaseSVC.decision_function``` when the `decision_function_shape` is set to `ovo`.

### Tree/Random Forest/XGBoost/LightGBM
#### Binary
Vector value; class probabilities.
#### Multiclass
Vector value; class probabilities.
#### Comment
The output is consistent with the output of the `predict_proba` method of `DecisionTreeClassifier`/`ForestClassifier`/`XGBClassifier`/`LGBMClassifier`.

## Usage

Here's a simple example of how a linear model trained in Python environment can be represented in Java code:
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

Generated Java code:
```java
public class Model {

    public static double score(double[] input) {
        return (((((((((((((36.45948838508965) + ((input[0]) * (-0.10801135783679647))) + ((input[1]) * (0.04642045836688297))) + ((input[2]) * (0.020558626367073608))) + ((input[3]) * (2.6867338193449406))) + ((input[4]) * (-17.76661122830004))) + ((input[5]) * (3.8098652068092163))) + ((input[6]) * (0.0006922246403454562))) + ((input[7]) * (-1.475566845600257))) + ((input[8]) * (0.30604947898516943))) + ((input[9]) * (-0.012334593916574394))) + ((input[10]) * (-0.9527472317072884))) + ((input[11]) * (0.009311683273794044))) + ((input[12]) * (-0.5247583778554867));
    }
}
```

**You can find more examples of generated code for different models/languages [here](https://github.com/BayesWitnesses/m2cgen/tree/master/generated_code_examples).**

## CLI

`m2cgen` can be used as a CLI tool to generate code using serialized model objects (pickle protocol):
```
$ m2cgen <pickle_file> --language <language> [--indent <indent>] [--class_name <class_name>]
         [--module_name <module_name>] [--package_name <package_name>] [--namespace <namespace>]
         [--recursion-limit <recursion_limit>]
```
Don't forget that for unpickling serialized model objects their classes must be defined in the top level of an importable module in the unpickling environment.

Piping is also supported:
```
$ cat <pickle_file> | m2cgen --language <language>
```

## FAQ
**Q: Generation fails with `RuntimeError: maximum recursion depth exceeded` error.**

A: If this error occurs while generating code using an ensemble model, try to reduce the number of trained estimators within that model. Alternatively you can increase the maximum recursion depth with `sys.setrecursionlimit(<new_depth>)`.

**Q: Generation fails with `ImportError: No module named <module_name_here>` error while transpiling model from a serialized model object.**

A: This error indicates that pickle protocol cannot deserialize model object. For unpickling serialized model objects, it is required that their classes must be defined in the top level of an importable module in the unpickling environment. So installation of package which provided model's class definition should solve the problem.
