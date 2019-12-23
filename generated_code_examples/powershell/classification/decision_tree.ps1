function Score([double[]] $InputVector) {
    [double[]]$var0 = @(0)
    if (($InputVector[2]) -le (2.6)) {
        $var0 = @($(1.0), $(0.0), $(0.0))
    } else {
        if (($InputVector[2]) -le (4.8500004)) {
            if (($InputVector[3]) -le (1.6500001)) {
                $var0 = @($(0.0), $(1.0), $(0.0))
            } else {
                $var0 = @($(0.0), $(0.3333333333333333), $(0.6666666666666666))
            }
        } else {
            if (($InputVector[3]) -le (1.75)) {
                $var0 = @($(0.0), $(0.42857142857142855), $(0.5714285714285714))
            } else {
                $var0 = @($(0.0), $(0.0), $(1.0))
            }
        }
    }
    return $var0
}
