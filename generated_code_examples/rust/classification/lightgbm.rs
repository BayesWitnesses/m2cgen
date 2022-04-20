fn score(input: Vec<f64>) -> Vec<f64> {
    let var0: f64;
    if input[2] > 3.1500000000000004_f64 {
        var0 = -1.1986122886681099_f64;
    } else {
        if input[1] > 3.35_f64 {
            var0 = -0.8986122886681098_f64;
        } else {
            var0 = -0.9136122886681098_f64;
        }
    }
    let var1: f64;
    if input[2] > 3.1500000000000004_f64 {
        if input[2] > 4.450000000000001_f64 {
            var1 = -0.09503010837903424_f64;
        } else {
            var1 = -0.09563272415214283_f64;
        }
    } else {
        if input[1] > 3.35_f64 {
            var1 = 0.16640323607832397_f64;
        } else {
            var1 = 0.15374604217339707_f64;
        }
    }
    let var2: f64;
    if input[2] > 1.8_f64 {
        if input[3] > 1.6500000000000001_f64 {
            var2 = -1.2055899476674514_f64;
        } else {
            var2 = -0.9500445227622534_f64;
        }
    } else {
        var2 = -1.2182214705715104_f64;
    }
    let var3: f64;
    if input[3] > 0.45000000000000007_f64 {
        if input[3] > 1.6500000000000001_f64 {
            var3 = -0.08146437273923739_f64;
        } else {
            var3 = 0.14244886188108738_f64;
        }
    } else {
        if input[2] > 1.4500000000000002_f64 {
            var3 = -0.0950888159264695_f64;
        } else {
            var3 = -0.09438233722389686_f64;
        }
    }
    let var4: f64;
    if input[3] > 1.6500000000000001_f64 {
        if input[2] > 5.3500000000000005_f64 {
            var4 = -0.8824095771015287_f64;
        } else {
            var4 = -0.9121126703829481_f64;
        }
    } else {
        if input[2] > 4.450000000000001_f64 {
            var4 = -1.1277829563828181_f64;
        } else {
            var4 = -1.1794405099157212_f64;
        }
    }
    let var5: f64;
    if input[2] > 4.750000000000001_f64 {
        if input[2] > 5.150000000000001_f64 {
            var5 = 0.16625543464258166_f64;
        } else {
            var5 = 0.09608601737074281_f64;
        }
    } else {
        if input[0] > 4.950000000000001_f64 {
            var5 = -0.09644547407948921_f64;
        } else {
            var5 = -0.08181864271444342_f64;
        }
    }
    softmax(vec![var0 + var1, var2 + var3, var4 + var5])
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
