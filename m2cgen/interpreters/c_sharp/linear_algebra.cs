private static double[] AddVectors(double[] v1, double[] v2) {
    double[] result = new double[v1.Length];
    for (int i = 0; i < v1.Length; ++i) {
        result[i] = v1[i] + v2[i];
    }
    return result;
}
private static double[] MulVectorNumber(double[] v1, double num) {
    double[] result = new double[v1.Length];
    for (int i = 0; i < v1.Length; ++i) {
        result[i] = v1[i] * num;
    }
    return result;
}
