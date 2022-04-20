fn score(input: Vec<f64>) -> Vec<f64> {
    let var0: f64;
    if input[2] >= 2.45_f64 {
        var0 = -0.21995015_f64;
    } else {
        var0 = 0.4302439_f64;
    }
    let var1: f64;
    if input[2] >= 2.45_f64 {
        var1 = -0.19691855_f64;
    } else {
        var1 = 0.29493433_f64;
    }
    let var2: f64;
    if input[2] >= 2.45_f64 {
        if input[3] >= 1.75_f64 {
            var2 = -0.20051816_f64;
        } else {
            var2 = 0.36912444_f64;
        }
    } else {
        var2 = -0.21512198_f64;
    }
    let var3: f64;
    if input[2] >= 2.45_f64 {
        if input[2] >= 4.8500004_f64 {
            var3 = -0.14888482_f64;
        } else {
            var3 = 0.2796613_f64;
        }
    } else {
        var3 = -0.19143805_f64;
    }
    let var4: f64;
    if input[3] >= 1.6500001_f64 {
        var4 = 0.40298507_f64;
    } else {
        if input[2] >= 4.95_f64 {
            var4 = 0.21724138_f64;
        } else {
            var4 = -0.21974029_f64;
        }
    }
    let var5: f64;
    if input[2] >= 4.75_f64 {
        if input[3] >= 1.75_f64 {
            var5 = 0.28692952_f64;
        } else {
            var5 = 0.06272897_f64;
        }
    } else {
        if input[3] >= 1.55_f64 {
            var5 = 0.009899145_f64;
        } else {
            var5 = -0.19659369_f64;
        }
    }
    softmax(vec![0.5_f64 + (var0 + var1), 0.5_f64 + (var2 + var3), 0.5_f64 + (var4 + var5)])
}
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
