public class Model {

    public static double[] score(double[] input) {
        return new double[] {subroutine0(input), subroutine1(input), subroutine2(input)};
    }
    public static double subroutine0(double[] input) {
        return ((((0.26145874358806076) + ((input[0]) * (0.4247411605356963))) + ((input[1]) * (1.3963906033045022))) + ((input[2]) * (-2.215054318516674))) + ((input[3]) * (-0.9587396176450291));
    }
    public static double subroutine1(double[] input) {
        return ((((1.1348839223808753) + ((input[0]) * (0.25679659769994584))) + ((input[1]) * (-1.3904789369835584))) + ((input[2]) * (0.5966830233112762))) + ((input[3]) * (-1.269002272638834));
    }
    public static double subroutine2(double[] input) {
        return ((((-1.2162802012560212) + ((input[0]) * (-1.6357766989177105))) + ((input[1]) * (-1.5040638728422817))) + ((input[2]) * (2.4278359331292716))) + ((input[3]) * (2.3469310693367236));
    }
}
