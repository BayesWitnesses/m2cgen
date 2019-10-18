public class Model {

    public static double[] score(double[] input) {
        return new double[] {subroutine0(input), subroutine1(input), subroutine2(input)};
    }
    public static double subroutine0(double[] input) {
        return ((((0.2614587435880605) + ((input[0]) * (0.42474116053569605))) + ((input[1]) * (1.3963906033045026))) + ((input[2]) * (-2.215054318516674))) + ((input[3]) * (-0.9587396176450289));
    }
    public static double subroutine1(double[] input) {
        return ((((1.1348839223808307) + ((input[0]) * (0.2567965976997648))) + ((input[1]) * (-1.3904789369836008))) + ((input[2]) * (0.596683023311173))) + ((input[3]) * (-1.2690022726388828));
    }
    public static double subroutine2(double[] input) {
        return ((((-1.2162802012560197) + ((input[0]) * (-1.6357766989177105))) + ((input[1]) * (-1.5040638728422817))) + ((input[2]) * (2.427835933129272))) + ((input[3]) * (2.3469310693367276));
    }
}
