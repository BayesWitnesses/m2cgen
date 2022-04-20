import "math"
func score(input []float64) []float64 {
    var var0 float64
    if input[2] >= 2.45 {
        var0 = -0.21995015
    } else {
        var0 = 0.4302439
    }
    var var1 float64
    if input[2] >= 2.45 {
        var1 = -0.19691855
    } else {
        var1 = 0.29493433
    }
    var var2 float64
    if input[2] >= 2.45 {
        if input[3] >= 1.75 {
            var2 = -0.20051816
        } else {
            var2 = 0.36912444
        }
    } else {
        var2 = -0.21512198
    }
    var var3 float64
    if input[2] >= 2.45 {
        if input[2] >= 4.8500004 {
            var3 = -0.14888482
        } else {
            var3 = 0.2796613
        }
    } else {
        var3 = -0.19143805
    }
    var var4 float64
    if input[3] >= 1.6500001 {
        var4 = 0.40298507
    } else {
        if input[2] >= 4.95 {
            var4 = 0.21724138
        } else {
            var4 = -0.21974029
        }
    }
    var var5 float64
    if input[2] >= 4.75 {
        if input[3] >= 1.75 {
            var5 = 0.28692952
        } else {
            var5 = 0.06272897
        }
    } else {
        if input[3] >= 1.55 {
            var5 = 0.009899145
        } else {
            var5 = -0.19659369
        }
    }
    return softmax([]float64{0.5 + (var0 + var1), 0.5 + (var2 + var3), 0.5 + (var4 + var5)})
}
func softmax(x []float64) []float64 {
    size := len(x)
    result := make([]float64, size)
    max := x[0]
    for _, v := range x {
        if (v > max) {
            max = v
        }
    }
    sum := 0.0
    for i := 0; i < size; i++ {
        result[i] = math.Exp(x[i] - max)
        sum += result[i]
    }
    for i := 0; i < size; i++ {
        result[i] /= sum
    }
    return result
}
