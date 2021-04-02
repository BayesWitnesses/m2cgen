List<double> addVectors(List<double> v1, List<double> v2) {
    List<double> result = new List<double>.filled(v1.length, 0.0);
    for (int i = 0; i < v1.length; i++) {
        result[i] = v1[i] + v2[i];
    }
    return result;
}
List<double> mulVectorNumber(List<double> v1, double num) {
    List<double> result = new List<double>.filled(v1.length, 0.0);
    for (int i = 0; i < v1.length; i++) {
        result[i] = v1[i] * num;
    }
    return result;
}
