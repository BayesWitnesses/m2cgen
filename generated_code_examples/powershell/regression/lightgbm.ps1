function Score([double[]] $InputVector) {
    [double]$var0 = 0
    if (($InputVector[5]) -gt (6.918000000000001)) {
        if (($InputVector[5]) -gt (7.437)) {
            $var0 = 24.81112131071211
        } else {
            $var0 = 23.5010290754961
        }
    } else {
        if (($InputVector[12]) -gt (14.365)) {
            $var0 = 21.796569516771488
        } else {
            $var0 = 22.640634908349323
        }
    }
    [double]$var1 = 0
    if (($InputVector[12]) -gt (9.63)) {
        if (($InputVector[12]) -gt (19.23)) {
            $var1 = -0.9218520876020193
        } else {
            $var1 = -0.30490175606373926
        }
    } else {
        if (($InputVector[5]) -gt (7.437)) {
            $var1 = 2.028554553190867
        } else {
            $var1 = 0.45970642160364367
        }
    }
    return ((0) + ($var0)) + ($var1)
}
