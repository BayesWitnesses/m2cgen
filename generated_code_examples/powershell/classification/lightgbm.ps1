function Score([double[]] $InputVector) {
    [double]$var0 = 0
    if (($InputVector[2]) -gt (1.8)) {
        if (($InputVector[2]) -gt (4.250000000000001)) {
            $var0 = -1.1736122903444903
        } else {
            $var0 = -1.1633850173886202
        }
    } else {
        $var0 = -0.9486122853153485
    }
    [double]$var1 = 0
    if (($InputVector[2]) -gt (1.8)) {
        if (($InputVector[1]) -gt (3.0500000000000003)) {
            $var1 = -0.06193194743580539
        } else {
            $var1 = -0.07237070828653688
        }
    } else {
        $var1 = 0.12984943093573026
    }
    [double]$var2 = 0
    $var2 = [math]::Exp(((0) + ($var0)) + ($var1))
    [double]$var3 = 0
    if (($InputVector[2]) -gt (1.8)) {
        if (($InputVector[2]) -gt (4.8500000000000005)) {
            $var3 = -1.1807342692411888
        } else {
            $var3 = -0.9831932134295853
        }
    } else {
        $var3 = -1.1952609652674462
    }
    [double]$var4 = 0
    if (($InputVector[2]) -gt (1.8)) {
        if (($InputVector[2]) -gt (4.8500000000000005)) {
            $var4 = -0.05694282927518771
        } else {
            $var4 = 0.11960489254350348
        }
    } else {
        $var4 = -0.07151978915296087
    }
    [double]$var5 = 0
    $var5 = [math]::Exp(((0) + ($var3)) + ($var4))
    [double]$var6 = 0
    if (($InputVector[2]) -gt (4.8500000000000005)) {
        if (($InputVector[3]) -gt (1.9500000000000002)) {
            $var6 = -0.9298942558407184
        } else {
            $var6 = -0.9632815288936335
        }
    } else {
        if (($InputVector[2]) -gt (4.250000000000001)) {
            $var6 = -1.1322413652523249
        } else {
            $var6 = -1.1524760761934856
        }
    }
    [double]$var7 = 0
    if (($InputVector[2]) -gt (4.8500000000000005)) {
        if (($InputVector[3]) -gt (1.9500000000000002)) {
            $var7 = 0.12809276954555665
        } else {
            $var7 = 0.09898817876916756
        }
    } else {
        if (($InputVector[2]) -gt (4.250000000000001)) {
            $var7 = -0.052710589717642864
        } else {
            $var7 = -0.07292857712854424
        }
    }
    [double]$var8 = 0
    $var8 = [math]::Exp(((0) + ($var6)) + ($var7))
    [double]$var9 = 0
    $var9 = (($var2) + ($var5)) + ($var8)
    return @($(($var2) / ($var9)), $(($var5) / ($var9)), $(($var8) / ($var9)))
}
