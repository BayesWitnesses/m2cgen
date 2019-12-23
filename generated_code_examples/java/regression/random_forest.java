public class Model {

    public static double score(double[] input) {
        return ((subroutine0(input)) * (0.5)) + ((subroutine1(input)) * (0.5));
    }
    public static double subroutine0(double[] input) {
        double var0;
        if ((input[12]) <= (8.91)) {
            if ((input[5]) <= (6.902)) {
                if ((input[7]) <= (1.48495)) {
                    var0 = 50.0;
                } else {
                    var0 = 25.320000000000004;
                }
            } else {
                var0 = 38.34810126582279;
            }
        } else {
            if ((input[0]) <= (5.84803)) {
                var0 = 19.99185520361991;
            } else {
                var0 = 12.102469135802467;
            }
        }
        return var0;
    }
    public static double subroutine1(double[] input) {
        double var0;
        if ((input[12]) <= (9.725)) {
            if ((input[5]) <= (7.4525)) {
                if ((input[5]) <= (6.7539997)) {
                    var0 = 24.801739130434775;
                } else {
                    var0 = 32.47230769230769;
                }
            } else {
                var0 = 47.075;
            }
        } else {
            if ((input[12]) <= (15.0)) {
                var0 = 20.44094488188976;
            } else {
                var0 = 14.823214285714291;
            }
        }
        return var0;
    }
}
