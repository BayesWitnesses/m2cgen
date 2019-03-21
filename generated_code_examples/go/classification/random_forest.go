func addVectors(v1, v2 []float64) []float64 {
    result := make([]float64, len(v1))
    for i := 0; i < len(v1); i++ {
        result[i] = v1[i] + v2[i]
    }
    return result
}
func mulVectorNumber(v1 []float64, num float64) []float64 {
    result := make([]float64, len(v1))
    for i := 0; i < len(v1); i++ {
        result[i] = v1[i] * num
    }
    return result
}
func score(input []float64) []float64 {
    var var0 []float64
    if (input[3]) <= (0.8) {
        var0 = []float64{1.0, 0.0, 0.0}
    } else {
        if (input[2]) <= (4.8500004) {
            var0 = []float64{0.0, 0.9795918367346939, 0.02040816326530612}
        } else {
            if (input[3]) <= (1.75) {
                if (input[3]) <= (1.6500001) {
                    var0 = []float64{0.0, 0.25, 0.75}
                } else {
                    var0 = []float64{0.0, 1.0, 0.0}
                }
            } else {
                var0 = []float64{0.0, 0.0, 1.0}
            }
        }
    }
    var var1 []float64
    if (input[3]) <= (0.8) {
        var1 = []float64{1.0, 0.0, 0.0}
    } else {
        if (input[0]) <= (6.05) {
            if (input[2]) <= (4.9) {
                var1 = []float64{0.0, 0.9032258064516129, 0.0967741935483871}
            } else {
                var1 = []float64{0.0, 0.0, 1.0}
            }
        } else {
            if (input[3]) <= (1.75) {
                var1 = []float64{0.0, 0.8, 0.2}
            } else {
                var1 = []float64{0.0, 0.0, 1.0}
            }
        }
    }
    return addVectors(mulVectorNumber(var0, 0.5), mulVectorNumber(var1, 0.5))
}
