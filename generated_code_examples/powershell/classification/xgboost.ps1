function Score([double[]] $InputVector) {
    [double]$var0 = 0
    if (($InputVector[2]) -ge (2.5999999)) {
        $var0 = -0.0731707439
    } else {
        $var0 = 0.142857149
    }
    [double]$var1 = 0
    if (($InputVector[2]) -ge (2.5999999)) {
        $var1 = -0.0705206916
    } else {
        $var1 = 0.12477719
    }
    [double]$var2 = 0
    $var2 = [math]::Exp(((0.5) + ($var0)) + ($var1))
    [double]$var3 = 0
    if (($InputVector[2]) -ge (2.5999999)) {
        if (($InputVector[2]) -ge (4.85000038)) {
            $var3 = -0.0578680299
        } else {
            $var3 = 0.132596686
        }
    } else {
        $var3 = -0.0714285821
    }
    [double]$var4 = 0
    if (($InputVector[2]) -ge (2.5999999)) {
        if (($InputVector[2]) -ge (4.85000038)) {
            $var4 = -0.0552999265
        } else {
            $var4 = 0.116139404
        }
    } else {
        $var4 = -0.0687687024
    }
    [double]$var5 = 0
    $var5 = [math]::Exp(((0.5) + ($var3)) + ($var4))
    [double]$var6 = 0
    if (($InputVector[2]) -ge (4.85000038)) {
        if (($InputVector[3]) -ge (1.75)) {
            $var6 = 0.142011836
        } else {
            $var6 = 0.0405405387
        }
    } else {
        if (($InputVector[3]) -ge (1.6500001)) {
            $var6 = 0.0428571403
        } else {
            $var6 = -0.0730659068
        }
    }
    [double]$var7 = 0
    if (($InputVector[2]) -ge (4.85000038)) {
        if (($InputVector[3]) -ge (1.75)) {
            $var7 = 0.124653697
        } else {
            $var7 = 0.035562478
        }
    } else {
        if (($InputVector[3]) -ge (1.6500001)) {
            $var7 = 0.0425687581
        } else {
            $var7 = -0.0704230517
        }
    }
    [double]$var8 = 0
    $var8 = [math]::Exp(((0.5) + ($var6)) + ($var7))
    [double]$var9 = 0
    $var9 = (($var2) + ($var5)) + ($var8)
    return @($(($var2) / ($var9)), $(($var5) / ($var9)), $(($var8) / ($var9)))
}
