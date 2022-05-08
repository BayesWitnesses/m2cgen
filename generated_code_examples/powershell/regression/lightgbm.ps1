function Score([double[]] $InputVector) {
    [double]$var0 = 0.0
    if ($InputVector[12] -gt 9.725000000000003) {
        if ($InputVector[12] -gt 16.205000000000002) {
            $var0 = 21.71499740307178
        } else {
            $var0 = 22.322292901846218
        }
    } else {
        if ($InputVector[5] -gt 7.418000000000001) {
            $var0 = 24.75760617150803
        } else {
            $var0 = 23.02910423871904
        }
    }
    [double]$var1 = 0.0
    if ($InputVector[5] -gt 6.837500000000001) {
        if ($InputVector[5] -gt 7.462000000000001) {
            $var1 = 2.0245964808123453
        } else {
            $var1 = 0.859548540618913
        }
    } else {
        if ($InputVector[12] -gt 14.365) {
            $var1 = -0.7009440524656984
        } else {
            $var1 = 0.052794864734003494
        }
    }
    return $var0 + $var1
}
