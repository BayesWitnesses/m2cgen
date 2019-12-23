public class Model {

    public static double[] score(double[] input) {
        return new double[] {subroutine0(input), subroutine1(input), subroutine2(input)};
    }
    public static double subroutine0(double[] input) {
        return ((((9.774126241420623) + ((input[0]) * (-0.41545978008486634))) + ((input[1]) * (0.9619661444337051))) + ((input[2]) * (-2.5028461157608604))) + ((input[3]) * (-1.0766107732916166));
    }
    public static double subroutine1(double[] input) {
        return ((((2.248771246116064) + ((input[0]) * (0.5239098915475155))) + ((input[1]) * (-0.3177027667958222))) + ((input[2]) * (-0.20333498652290763))) + ((input[3]) * (-0.9399605394445277));
    }
    public static double subroutine2(double[] input) {
        return ((((-12.022897487538232) + ((input[0]) * (-0.10845011146263966))) + ((input[1]) * (-0.6442633776378855))) + ((input[2]) * (2.7061811022837774))) + ((input[3]) * (2.01657131273614));
    }
}
