function Score([double[]] $InputVector) {
    [double]$var0 = 0
    if (($InputVector[5]) -le (6.941)) {
        if (($InputVector[12]) -le (14.4)) {
            if (($InputVector[7]) -le (1.38485)) {
                $var0 = 45.58
            } else {
                $var0 = 22.939004149377574
            }
        } else {
            $var0 = 14.910404624277467
        }
    } else {
        if (($InputVector[5]) -le (7.4370003)) {
            $var0 = 32.11304347826088
        } else {
            $var0 = 45.096666666666664
        }
    }
    return $var0
}
