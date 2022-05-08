function Score([double[]] $InputVector) {
    [double]$var0 = 0.0
    if ($InputVector[12] -le 9.724999904632568) {
        if ($InputVector[5] -le 7.437000036239624) {
            if ($InputVector[7] -le 1.4849499464035034) {
                $var0 = 50.0
            } else {
                $var0 = 26.681034482758605
            }
        } else {
            $var0 = 44.96896551724139
        }
    } else {
        if ($InputVector[12] -le 16.085000038146973) {
            $var0 = 20.284353741496595
        } else {
            $var0 = 14.187142857142863
        }
    }
    return $var0
}
