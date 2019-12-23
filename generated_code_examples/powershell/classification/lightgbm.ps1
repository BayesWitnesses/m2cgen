function Score([double[]] $InputVector) {
    [double]$var0 = 0
    if (($InputVector[2]) -gt (3.1500000000000004)) {
        $var0 = -1.1736122903444903
    } else {
        if (($InputVector[1]) -gt (3.35)) {
            $var0 = -0.9486122853153485
        } else {
            $var0 = -0.9598622855668056
        }
    }
    [double]$var1 = 0
    if (($InputVector[2]) -gt (3.1500000000000004)) {
        if (($InputVector[2]) -gt (4.450000000000001)) {
            $var1 = -0.07218200074594171
        } else {
            $var1 = -0.0725391787456957
        }
    } else {
        if (($InputVector[1]) -gt (3.35)) {
            $var1 = 0.130416969124648
        } else {
            $var1 = 0.12058330491181404
        }
    }
    [double]$var2 = 0
    $var2 = [math]::Exp(((0) + ($var0)) + ($var1))
    [double]$var3 = 0
    if (($InputVector[2]) -gt (1.8)) {
        if (($InputVector[3]) -gt (1.6500000000000001)) {
            $var3 = -1.1840003561812273
        } else {
            $var3 = -0.99234128317334
        }
    } else {
        $var3 = -1.1934739985732523
    }
    [double]$var4 = 0
    if (($InputVector[3]) -gt (0.45000000000000007)) {
        if (($InputVector[3]) -gt (1.6500000000000001)) {
            $var4 = -0.06203313079859976
        } else {
            $var4 = 0.11141505233015861
        }
    } else {
        if (($InputVector[2]) -gt (1.4500000000000002)) {
            $var4 = -0.0720353255122301
        } else {
            $var4 = -0.07164473223425313
        }
    }
    [double]$var5 = 0
    $var5 = [math]::Exp(((0) + ($var3)) + ($var4))
    [double]$var6 = 0
    if (($InputVector[3]) -gt (1.6500000000000001)) {
        if (($InputVector[2]) -gt (5.3500000000000005)) {
            $var6 = -0.9314095846701695
        } else {
            $var6 = -0.9536869036452162
        }
    } else {
        if (($InputVector[2]) -gt (4.450000000000001)) {
            $var6 = -1.115439610985773
        } else {
            $var6 = -1.1541827744206368
        }
    }
    [double]$var7 = 0
    if (($InputVector[2]) -gt (4.750000000000001)) {
        if (($InputVector[2]) -gt (5.150000000000001)) {
            $var7 = 0.12968922424213622
        } else {
            $var7 = 0.07468384042736965
        }
    } else {
        if (($InputVector[1]) -gt (2.7500000000000004)) {
            $var7 = -0.07311533184609437
        } else {
            $var7 = -0.06204412771870974
        }
    }
    [double]$var8 = 0
    $var8 = [math]::Exp(((0) + ($var6)) + ($var7))
    [double]$var9 = 0
    $var9 = (($var2) + ($var5)) + ($var8)
    return @($(($var2) / ($var9)), $(($var5) / ($var9)), $(($var8) / ($var9)))
}
