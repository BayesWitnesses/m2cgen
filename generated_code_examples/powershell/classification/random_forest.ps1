function Score([double[]] $InputVector) {
    [double[]]$var0 = @(0.0)
    if ($InputVector[3] -le 0.75) {
        $var0 = @($(1.0), $(0.0), $(0.0))
    } else {
        if ($InputVector[2] -le 4.75) {
            $var0 = @($(0.0), $(1.0), $(0.0))
        } else {
            if ($InputVector[2] -le 5.049999952316284) {
                if ($InputVector[3] -le 1.75) {
                    $var0 = @($(0.0), $(0.8333333333333334), $(0.16666666666666666))
                } else {
                    $var0 = @($(0.0), $(0.08333333333333333), $(0.9166666666666666))
                }
            } else {
                $var0 = @($(0.0), $(0.0), $(1.0))
            }
        }
    }
    [double[]]$var1 = @(0.0)
    if ($InputVector[3] -le 0.800000011920929) {
        $var1 = @($(1.0), $(0.0), $(0.0))
    } else {
        if ($InputVector[0] -le 6.25) {
            if ($InputVector[2] -le 4.8500001430511475) {
                $var1 = @($(0.0), $(0.9487179487179487), $(0.05128205128205128))
            } else {
                $var1 = @($(0.0), $(0.0), $(1.0))
            }
        } else {
            if ($InputVector[3] -le 1.550000011920929) {
                $var1 = @($(0.0), $(0.8333333333333334), $(0.16666666666666666))
            } else {
                $var1 = @($(0.0), $(0.02564102564102564), $(0.9743589743589743))
            }
        }
    }
    return Mul-Vector-Number $(Add-Vectors $($var0) $($var1)) $(0.5)
}
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
