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
        return ((0.5) + (subroutine3(input))) + (subroutine4(input));
    }
    public static double subroutine1(double[] input) {
        return ((0.5) + (subroutine5(input))) + (subroutine6(input));
    }
    public static double subroutine2(double[] input) {
        return ((0.5) + (subroutine7(input))) + (subroutine8(input));
    }
    public static double subroutine3(double[] input) {
        double var0;
        if ((input[2]) >= (2.45000005)) {
            var0 = -0.0733167157;
        } else {
            var0 = 0.143414631;
        }
        return var0;
    }
    public static double subroutine4(double[] input) {
        double var0;
        if ((input[2]) >= (2.45000005)) {
            var0 = -0.0706516728;
        } else {
            var0 = 0.125176534;
        }
        return var0;
    }
    public static double subroutine5(double[] input) {
        double var0;
        if ((input[2]) >= (2.45000005)) {
            if ((input[3]) >= (1.75)) {
                var0 = -0.0668393895;
            } else {
                var0 = 0.123041473;
            }
        } else {
            var0 = -0.0717073306;
        }
        return var0;
    }
    public static double subroutine6(double[] input) {
        double var0;
        if ((input[2]) >= (2.45000005)) {
            if ((input[3]) >= (1.75)) {
                var0 = -0.0642274022;
            } else {
                var0 = 0.10819874;
            }
        } else {
            var0 = -0.069036141;
        }
        return var0;
    }
    public static double subroutine7(double[] input) {
        double var0;
        if ((input[3]) >= (1.6500001)) {
            var0 = 0.13432835;
        } else {
            if ((input[2]) >= (4.94999981)) {
                var0 = 0.0724137947;
            } else {
                var0 = -0.0732467622;
            }
        }
        return var0;
    }
    public static double subroutine8(double[] input) {
        double var0;
        if ((input[3]) >= (1.6500001)) {
            var0 = 0.117797568;
        } else {
            if ((input[2]) >= (4.94999981)) {
                var0 = 0.0702545047;
            } else {
                var0 = -0.0706570372;
            }
        }
        return var0;
    }
}
