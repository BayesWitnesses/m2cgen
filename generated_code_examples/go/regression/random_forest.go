func score(input []float64) float64 {
    var var0 float64
    if input[12] <= 9.845000267028809 {
        if input[5] <= 6.959500074386597 {
            if input[6] <= 96.20000076293945 {
                var0 = 25.093162393162395
            } else {
                var0 = 50.0
            }
        } else {
            var0 = 38.074999999999996
        }
    } else {
        if input[12] <= 15.074999809265137 {
            var0 = 20.518439716312056
        } else {
            var0 = 14.451282051282046
        }
    }
    var var1 float64
    if input[12] <= 9.650000095367432 {
        if input[5] <= 7.437000036239624 {
            if input[7] <= 1.47284996509552 {
                var1 = 50.0
            } else {
                var1 = 26.7965317919075
            }
        } else {
            var1 = 44.21176470588236
        }
    } else {
        if input[12] <= 17.980000495910645 {
            var1 = 19.645652173913035
        } else {
            var1 = 12.791919191919195
        }
    }
    return (var0 + var1) * 0.5
}
