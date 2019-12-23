function Add-Vectors([double[]] $v1, [double[]] $v2) {
    [int] $length = $v1.Length
    [double[]] $result = @(0) * $length
    for ([int] $i = 0; $i -lt $length; ++$i) {
        $result[$i] = $v1[$i] + $v2[$i]
    }
    return $result
}
function Mul-Vector-Number([double[]] $v1, [double] $num) {
    [int] $length = $v1.Length
    [double[]] $result = @(0) * $length
    for ([int] $i = 0; $i -lt $length; ++$i) {
        $result[$i] = $v1[$i] * $num
    }
    return $result
}
function Score([double[]] $InputVector) {
    [double[]]$var0 = @(0)
    if (($InputVector[3]) -le (0.8)) {
        $var0 = @($(1.0), $(0.0), $(0.0))
    } else {
        if (($InputVector[2]) -le (4.8500004)) {
            $var0 = @($(0.0), $(0.9622641509433962), $(0.03773584905660377))
        } else {
            if (($InputVector[3]) -le (1.75)) {
                if (($InputVector[3]) -le (1.6500001)) {
                    $var0 = @($(0.0), $(0.25), $(0.75))
                } else {
                    $var0 = @($(0.0), $(1.0), $(0.0))
                }
            } else {
                $var0 = @($(0.0), $(0.0), $(1.0))
            }
        }
    }
    [double[]]$var1 = @(0)
    if (($InputVector[3]) -le (0.8)) {
        $var1 = @($(1.0), $(0.0), $(0.0))
    } else {
        if (($InputVector[0]) -le (6.1499996)) {
            if (($InputVector[2]) -le (4.8500004)) {
                $var1 = @($(0.0), $(0.9090909090909091), $(0.09090909090909091))
            } else {
                $var1 = @($(0.0), $(0.0), $(1.0))
            }
        } else {
            if (($InputVector[3]) -le (1.75)) {
                $var1 = @($(0.0), $(0.8666666666666667), $(0.13333333333333333))
            } else {
                $var1 = @($(0.0), $(0.0), $(1.0))
            }
        }
    }
    return Add-Vectors $(Mul-Vector-Number $($var0) $(0.5)) $(Mul-Vector-Number $($var1) $(0.5))
}
