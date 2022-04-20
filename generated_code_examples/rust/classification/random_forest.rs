fn score(input: Vec<f64>) -> Vec<f64> {
    let var0: Vec<f64>;
    if input[3] <= 0.75_f64 {
        var0 = vec![1.0_f64, 0.0_f64, 0.0_f64];
    } else {
        if input[2] <= 4.75_f64 {
            var0 = vec![0.0_f64, 1.0_f64, 0.0_f64];
        } else {
            if input[2] <= 5.049999952316284_f64 {
                if input[3] <= 1.75_f64 {
                    var0 = vec![0.0_f64, 0.8333333333333334_f64, 0.16666666666666666_f64];
                } else {
                    var0 = vec![0.0_f64, 0.08333333333333333_f64, 0.9166666666666666_f64];
                }
            } else {
                var0 = vec![0.0_f64, 0.0_f64, 1.0_f64];
            }
        }
    }
    let var1: Vec<f64>;
    if input[3] <= 0.800000011920929_f64 {
        var1 = vec![1.0_f64, 0.0_f64, 0.0_f64];
    } else {
        if input[0] <= 6.25_f64 {
            if input[2] <= 4.8500001430511475_f64 {
                var1 = vec![0.0_f64, 0.9487179487179487_f64, 0.05128205128205128_f64];
            } else {
                var1 = vec![0.0_f64, 0.0_f64, 1.0_f64];
            }
        } else {
            if input[3] <= 1.550000011920929_f64 {
                var1 = vec![0.0_f64, 0.8333333333333334_f64, 0.16666666666666666_f64];
            } else {
                var1 = vec![0.0_f64, 0.02564102564102564_f64, 0.9743589743589743_f64];
            }
        }
    }
    mul_vector_number(add_vectors(var0, var1), 0.5_f64)
}
fn add_vectors(v1: Vec<f64>, v2: Vec<f64>) -> Vec<f64> {
    v1.iter().zip(v2.iter()).map(|(&x, &y)| x + y).collect::<Vec<f64>>()
}
fn mul_vector_number(v1: Vec<f64>, num: f64) -> Vec<f64> {
    v1.iter().map(|&i| i * num).collect::<Vec<f64>>()
}
