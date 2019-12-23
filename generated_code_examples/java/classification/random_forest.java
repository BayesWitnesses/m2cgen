public class Model {

    public static double[] score(double[] input) {
        return addVectors(mulVectorNumber(subroutine0(input), 0.5), mulVectorNumber(subroutine1(input), 0.5));
    }
    public static double[] subroutine0(double[] input) {
        double[] var0;
        if ((input[3]) <= (0.8)) {
            var0 = new double[] {1.0, 0.0, 0.0};
        } else {
            if ((input[2]) <= (4.8500004)) {
                var0 = new double[] {0.0, 0.9622641509433962, 0.03773584905660377};
            } else {
                if ((input[3]) <= (1.75)) {
                    if ((input[3]) <= (1.6500001)) {
                        var0 = new double[] {0.0, 0.25, 0.75};
                    } else {
                        var0 = new double[] {0.0, 1.0, 0.0};
                    }
                } else {
                    var0 = new double[] {0.0, 0.0, 1.0};
                }
            }
        }
        return var0;
    }
    public static double[] subroutine1(double[] input) {
        double[] var0;
        if ((input[3]) <= (0.8)) {
            var0 = new double[] {1.0, 0.0, 0.0};
        } else {
            if ((input[0]) <= (6.1499996)) {
                if ((input[2]) <= (4.8500004)) {
                    var0 = new double[] {0.0, 0.9090909090909091, 0.09090909090909091};
                } else {
                    var0 = new double[] {0.0, 0.0, 1.0};
                }
            } else {
                if ((input[3]) <= (1.75)) {
                    var0 = new double[] {0.0, 0.8666666666666667, 0.13333333333333333};
                } else {
                    var0 = new double[] {0.0, 0.0, 1.0};
                }
            }
        }
        return var0;
    }
    public static double[] addVectors(double[] v1, double[] v2) {
        double[] result = new double[v1.length];
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] + v2[i];
        }
        return result;
    }
    public static double[] mulVectorNumber(double[] v1, double num) {
        double[] result = new double[v1.length];
        for (int i = 0; i < v1.length; i++) {
            result[i] = v1[i] * num;
        }
        return result;
    }
}
