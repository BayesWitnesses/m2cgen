function Score([double[]] $InputVector) {
    [double]$var0 = 0
    if (($InputVector[5]) -le (6.92)) {
        if (($InputVector[12]) -le (14.3)) {
            if (($InputVector[7]) -le (1.47415)) {
                $var0 = 50.0
            } else {
                $var0 = 23.203669724770638
            }
        } else {
            $var0 = 15.177333333333326
        }
    } else {
        if (($InputVector[5]) -le (7.4370003)) {
            $var0 = 32.92407407407408
        } else {
            $var0 = 45.04827586206897
        }
    }
    [double]$var1 = 0
    if (($InputVector[12]) -le (9.725)) {
        if (($InputVector[5]) -le (7.4525)) {
            if (($InputVector[5]) -le (6.7539997)) {
                $var1 = 24.805
            } else {
                $var1 = 32.55238095238095
            }
        } else {
            $var1 = 47.88333333333334
        }
    } else {
        if (($InputVector[12]) -le (15.0)) {
            $var1 = 20.52100840336134
        } else {
            $var1 = 14.718709677419358
        }
    }
    return (($var0) * (0.5)) + (($var1) * (0.5))
}
