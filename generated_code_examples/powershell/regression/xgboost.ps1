function Score([double[]] $InputVector) {
    [double]$var0 = 0
    if (($InputVector[12]) -ge (9.72500038)) {
        if (($InputVector[12]) -ge (16.0849991)) {
            $var0 = 1.36374998
        } else {
            $var0 = 1.96335626
        }
    } else {
        if (($InputVector[5]) -ge (6.94099998)) {
            $var0 = 3.74704218
        } else {
            $var0 = 2.48376822
        }
    }
    [double]$var1 = 0
    if (($InputVector[12]) -ge (9.63000011)) {
        if (($InputVector[12]) -ge (19.2299995)) {
            $var1 = 1.05852115
        } else {
            $var1 = 1.68638802
        }
    } else {
        if (($InputVector[5]) -ge (7.43700027)) {
            $var1 = 3.95318961
        } else {
            $var1 = 2.40278864
        }
    }
    return ((0.5) + ($var0)) + ($var1)
}
