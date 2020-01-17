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
        return ((0) + (subroutine3(input))) + (subroutine4(input));
    }
    public static double subroutine1(double[] input) {
        return ((0) + (subroutine5(input))) + (subroutine6(input));
    }
    public static double subroutine2(double[] input) {
        return ((0) + (subroutine7(input))) + (subroutine8(input));
    }
    public static double subroutine3(double[] input) {
        double var0;
        if ((input[2]) > (3.1500000000000004)) {
            var0 = -1.1736122903444903;
        } else {
            if ((input[1]) > (3.35)) {
                var0 = -0.9486122853153485;
            } else {
                var0 = -0.9598622855668056;
            }
        }
        return var0;
    }
    public static double subroutine4(double[] input) {
        double var0;
        if ((input[2]) > (3.1500000000000004)) {
            if ((input[2]) > (4.450000000000001)) {
                var0 = -0.07218200074594171;
            } else {
                var0 = -0.0725391787456957;
            }
        } else {
            if ((input[1]) > (3.35)) {
                var0 = 0.130416969124648;
            } else {
                var0 = 0.12058330491181404;
            }
        }
        return var0;
    }
    public static double subroutine5(double[] input) {
        double var0;
        if ((input[2]) > (1.8)) {
            if ((input[3]) > (1.6500000000000001)) {
                var0 = -1.1840003561812273;
            } else {
                var0 = -0.99234128317334;
            }
        } else {
            var0 = -1.1934739985732523;
        }
        return var0;
    }
    public static double subroutine6(double[] input) {
        double var0;
        if ((input[3]) > (0.45000000000000007)) {
            if ((input[3]) > (1.6500000000000001)) {
                var0 = -0.06203313079859976;
            } else {
                var0 = 0.11141505233015861;
            }
        } else {
            if ((input[2]) > (1.4500000000000002)) {
                var0 = -0.0720353255122301;
            } else {
                var0 = -0.07164473223425313;
            }
        }
        return var0;
    }
    public static double subroutine7(double[] input) {
        double var0;
        if ((input[3]) > (1.6500000000000001)) {
            if ((input[2]) > (5.3500000000000005)) {
                var0 = -0.9314095846701695;
            } else {
                var0 = -0.9536869036452162;
            }
        } else {
            if ((input[2]) > (4.450000000000001)) {
                var0 = -1.115439610985773;
            } else {
                var0 = -1.1541827744206368;
            }
        }
        return var0;
    }
    public static double subroutine8(double[] input) {
        double var0;
        if ((input[2]) > (4.750000000000001)) {
            if ((input[2]) > (5.150000000000001)) {
                var0 = 0.12968922424213622;
            } else {
                var0 = 0.07468384042736965;
            }
        } else {
            if ((input[1]) > (2.7500000000000004)) {
                var0 = -0.07311533184609437;
            } else {
                var0 = -0.06204412771870974;
            }
        }
        return var0;
    }
}
