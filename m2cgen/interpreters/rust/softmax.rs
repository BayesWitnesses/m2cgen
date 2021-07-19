fn softmax(x: Vec<f64>) -> Vec<f64> {
    let size: usize = x.len();
    let m: f64 = x.iter().fold(std::f64::MIN, |a, b| a.max(*b));
    let mut exps: Vec<f64> = vec![0.0_f64; size];
    let mut s: f64 = 0.0_f64;
    for (i, &v) in x.iter().enumerate() {
        exps[i] = (v - m).exp();
        s += exps[i];
    }
    exps.iter().map(|&i| i / s).collect::<Vec<f64>>()
}
