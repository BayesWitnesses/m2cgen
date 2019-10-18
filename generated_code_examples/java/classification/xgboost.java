public class Model {

    public static double[] score(double[] input) {
        double var0;
        var0 = Math.exp(subroutine0(input));
        double var1;
        var1 = Math.exp(subroutine1(input));
        double var2;
        var2 = Math.exp(subroutine2(input));
        double var3;
        var3 = ((var0) + (var1)) + (var2);
        return new double[] {(var0) / (var3), (var1) / (var3), (var2) / (var3)};
    }
    public static double subroutine0(double[] input) {
        double var0;
        if ((input[2]) >= (2.5999999)) {
            var0 = -0.0731707439;
        } else {
            var0 = 0.142857149;
        }
        double var1;
        if ((input[2]) >= (2.5999999)) {
            var1 = -0.0705206916;
        } else {
            var1 = 0.12477719;
        }
        return ((0.5) + (var0)) + (var1);
    }
    public static double subroutine1(double[] input) {
        double var0;
        if ((input[2]) >= (2.5999999)) {
            if ((input[2]) >= (4.85000038)) {
                var0 = -0.0578680299;
            } else {
                var0 = 0.132596686;
            }
        } else {
            var0 = -0.0714285821;
        }
        double var1;
        if ((input[2]) >= (2.5999999)) {
            if ((input[2]) >= (4.85000038)) {
                var1 = -0.0552999265;
            } else {
                var1 = 0.116139404;
            }
        } else {
            var1 = -0.0687687024;
        }
        return ((0.5) + (var0)) + (var1);
    }
    public static double subroutine2(double[] input) {
        double var0;
        if ((input[2]) >= (4.85000038)) {
            if ((input[3]) >= (1.75)) {
                var0 = 0.142011836;
            } else {
                var0 = 0.0405405387;
            }
        } else {
            if ((input[3]) >= (1.6500001)) {
                var0 = 0.0428571403;
            } else {
                var0 = -0.0730659068;
            }
        }
        double var1;
        if ((input[2]) >= (4.85000038)) {
            if ((input[3]) >= (1.75)) {
                var1 = 0.124653697;
            } else {
                var1 = 0.035562478;
            }
        } else {
            if ((input[3]) >= (1.6500001)) {
                var1 = 0.0425687581;
            } else {
                var1 = -0.0704230517;
            }
        }
        return ((0.5) + (var0)) + (var1);
    }
}
