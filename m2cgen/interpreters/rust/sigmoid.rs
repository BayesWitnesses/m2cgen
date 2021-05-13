fn sigmoid(x: f64) -> f64 {
    if x < 0.0_f64 {
        let z: f64 = x.exp();
        return z / (1.0_f64 + z);
    }
    return 1.0_f64 / (1.0_f64 + (-x).exp());
}
