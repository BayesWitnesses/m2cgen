import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;
import java.util.Arrays;

class Executor {

    /** The example invocation: java -cp . Executor Model score 1 2 3 4 5 6 7 8 9 10 11 12 13 */
    public static void main(String[] args) {
        String className = args[0];
        String methodName = args[1];

        double[] features = new double[args.length-2];

        for (int i = 2, l = args.length; i < l; i++) {
            features[i-2] = Double.parseDouble(args[i]);
        }

        try {
            Class<?> klass = Class.forName(className);
            Method method = klass.getMethod(methodName, new Class[]{double[].class});
            Object result = method.invoke(null, features);
            if (result instanceof double[]) {
                double[] arr = (double[]) result;
                String out = "";
                for (int i = 0, l = arr.length; i < l; i++) {
                    out += arr[i];
                    out += " ";
                }
                System.out.println(out);
            } else {
                System.out.println(result);
            }
        } catch (ClassNotFoundException | NoSuchMethodException | IllegalAccessException | InvocationTargetException e) {
            e.printStackTrace();
        }
    }
}
