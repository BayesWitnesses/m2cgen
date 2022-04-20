function Score([double[]] $InputVector) {
    [double]$var0 = 0.0
    if ($InputVector[12] -le 9.845000267028809) {
        if ($InputVector[5] -le 6.959500074386597) {
            if ($InputVector[6] -le 96.20000076293945) {
                $var0 = 25.093162393162395
            } else {
                $var0 = 50.0
            }
        } else {
            $var0 = 38.074999999999996
        }
    } else {
        if ($InputVector[12] -le 15.074999809265137) {
            $var0 = 20.518439716312056
        } else {
            $var0 = 14.451282051282046
        }
    }
    [double]$var1 = 0.0
    if ($InputVector[12] -le 9.650000095367432) {
        if ($InputVector[5] -le 7.437000036239624) {
            if ($InputVector[7] -le 1.47284996509552) {
                $var1 = 50.0
            } else {
                $var1 = 26.7965317919075
            }
        } else {
            $var1 = 44.21176470588236
        }
    } else {
        if ($InputVector[12] -le 17.980000495910645) {
            $var1 = 19.645652173913035
        } else {
            $var1 = 12.791919191919195
        }
    }
    return ($var0 + $var1) * 0.5
}
