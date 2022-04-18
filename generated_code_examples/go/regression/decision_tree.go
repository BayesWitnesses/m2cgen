func score(input []float64) float64 {
    var var0 float64
    if input[12] <= 9.724999904632568 {
        if input[5] <= 7.437000036239624 {
            if input[7] <= 1.4849499464035034 {
                var0 = 50.0
            } else {
                var0 = 26.681034482758605
            }
        } else {
            var0 = 44.96896551724139
        }
    } else {
        if input[12] <= 16.085000038146973 {
            var0 = 20.284353741496595
        } else {
            var0 = 14.187142857142863
        }
    }
    return var0
}
