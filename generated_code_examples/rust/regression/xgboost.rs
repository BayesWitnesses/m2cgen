fn score(input: Vec<f64>) -> f64 {
    let var0: f64;
    if input[12] >= 9.725_f64 {
        if input[12] >= 19.23_f64 {
            var0 = 3.5343752_f64;
        } else {
            var0 = 5.5722494_f64;
        }
    } else {
        if input[5] >= 6.941_f64 {
            var0 = 11.1947155_f64;
        } else {
            var0 = 7.4582143_f64;
        }
    }
    let var1: f64;
    if input[12] >= 5.1549997_f64 {
        if input[12] >= 15.0_f64 {
            var1 = 2.8350503_f64;
        } else {
            var1 = 4.8024607_f64;
        }
    } else {
        if input[5] >= 7.406_f64 {
            var1 = 10.0011215_f64;
        } else {
            var1 = 6.787523_f64;
        }
    }
    0.5_f64 + (var0 + var1)
}
