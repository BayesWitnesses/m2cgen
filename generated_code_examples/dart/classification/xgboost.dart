import 'dart:math';
List<double> score(List<double> input) {
    double var0;
    if (input[2] >= 2.45) {
        var0 = -0.21995015;
    } else {
        var0 = 0.4302439;
    }
    double var1;
    if (input[2] >= 2.45) {
        var1 = -0.19691855;
    } else {
        var1 = 0.29493433;
    }
    double var2;
    if (input[2] >= 2.45) {
        if (input[3] >= 1.75) {
            var2 = -0.20051816;
        } else {
            var2 = 0.36912444;
        }
    } else {
        var2 = -0.21512198;
    }
    double var3;
    if (input[2] >= 2.45) {
        if (input[2] >= 4.8500004) {
            var3 = -0.14888482;
        } else {
            var3 = 0.2796613;
        }
    } else {
        var3 = -0.19143805;
    }
    double var4;
    if (input[3] >= 1.6500001) {
        var4 = 0.40298507;
    } else {
        if (input[2] >= 4.95) {
            var4 = 0.21724138;
        } else {
            var4 = -0.21974029;
        }
    }
    double var5;
    if (input[2] >= 4.75) {
        if (input[3] >= 1.75) {
            var5 = 0.28692952;
        } else {
            var5 = 0.06272897;
        }
    } else {
        if (input[3] >= 1.55) {
            var5 = 0.009899145;
        } else {
            var5 = -0.19659369;
        }
    }
    return softmax([0.5 + (var0 + var1), 0.5 + (var2 + var3), 0.5 + (var4 + var5)]);
}
List<double> softmax(List<double> x) {
    int size = x.length;
    List<double> result = new List<double>.filled(size, 0.0);
    double maxElem = x.reduce(max);
    double sum = 0.0;
    for (int i = 0; i < size; ++i) {
        result[i] = exp(x[i] - maxElem);
        sum += result[i];
    }
    for (int i = 0; i < size; ++i)
        result[i] /= sum;
    return result;
}
