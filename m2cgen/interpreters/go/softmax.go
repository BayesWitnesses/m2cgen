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
