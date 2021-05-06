func sigmoid(x float64) float64 {
    if (x < 0.0) {
        z := math.Exp(x)
        return z / (1.0 + z)
    }
    return 1.0 / (1.0 + math.Exp(-x))
}
