function Score([double[]] $InputVector) {
    [double]$var0 = 0.0
    if ($InputVector[12] -ge 9.725) {
        if ($InputVector[12] -ge 19.23) {
            $var0 = 3.5343752
        } else {
            $var0 = 5.5722494
        }
    } else {
        if ($InputVector[5] -ge 6.941) {
            $var0 = 11.1947155
        } else {
            $var0 = 7.4582143
        }
    }
    [double]$var1 = 0.0
    if ($InputVector[12] -ge 5.1549997) {
        if ($InputVector[12] -ge 15.0) {
            $var1 = 2.8350503
        } else {
            $var1 = 4.8024607
        }
    } else {
        if ($InputVector[5] -ge 7.406) {
            $var1 = 10.0011215
        } else {
            $var1 = 6.787523
        }
    }
    return 0.5 + ($var0 + $var1)
}
