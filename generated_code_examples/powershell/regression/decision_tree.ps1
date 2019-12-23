function Score([double[]] $InputVector) {
    [double]$var0 = 0
    if (($InputVector[5]) -le (6.941)) {
        if (($InputVector[12]) -le (14.395)) {
            if (($InputVector[7]) -le (1.43365)) {
                $var0 = 45.58
            } else {
                $var0 = 22.865022421524642
            }
        } else {
            $var0 = 14.924358974358983
        }
    } else {
        if (($InputVector[5]) -le (7.4370003)) {
            $var0 = 32.09534883720931
        } else {
            $var0 = 45.275
        }
    }
    return $var0
}
