function Score([double[]] $InputVector) {
    [double]$var0 = 0
    if (($InputVector[12]) -ge (9.72500038)) {
        if (($InputVector[12]) -ge (19.8299999)) {
            $var0 = 1.1551429
        } else {
            $var0 = 1.8613131
        }
    } else {
        if (($InputVector[5]) -ge (6.94099998)) {
            $var0 = 3.75848508
        } else {
            $var0 = 2.48056006
        }
    }
    [double]$var1 = 0
    if (($InputVector[12]) -ge (7.68499994)) {
        if (($InputVector[12]) -ge (15)) {
            $var1 = 1.24537706
        } else {
            $var1 = 1.92129695
        }
    } else {
        if (($InputVector[5]) -ge (7.43700027)) {
            $var1 = 3.96021533
        } else {
            $var1 = 2.51493931
        }
    }
    return ((0.5) + ($var0)) + ($var1)
}
