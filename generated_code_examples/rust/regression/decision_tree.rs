fn score(input: Vec<f64>) -> f64 {
    let var0: f64;
    if (input[12]) <= (9.724999904632568_f64) {
        if (input[5]) <= (7.437000036239624_f64) {
            if (input[7]) <= (1.4849499464035034_f64) {
                var0 = 50.0_f64;
            } else {
                var0 = 26.681034482758605_f64;
            }
        } else {
            var0 = 44.96896551724139_f64;
        }
    } else {
        if (input[12]) <= (16.085000038146973_f64) {
            var0 = 20.284353741496595_f64;
        } else {
            var0 = 14.187142857142863_f64;
        }
    }
    return var0;
}
