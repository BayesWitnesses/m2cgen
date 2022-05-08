function Score([double[]] $InputVector) {
    [double]$var0 = 0.0
    if ($InputVector[2] -ge 2.45) {
        $var0 = -0.21995015
    } else {
        $var0 = 0.4302439
    }
    [double]$var1 = 0.0
    if ($InputVector[2] -ge 2.45) {
        $var1 = -0.19691855
    } else {
        $var1 = 0.29493433
    }
    [double]$var2 = 0.0
    if ($InputVector[2] -ge 2.45) {
        if ($InputVector[3] -ge 1.75) {
            $var2 = -0.20051816
        } else {
            $var2 = 0.36912444
        }
    } else {
        $var2 = -0.21512198
    }
    [double]$var3 = 0.0
    if ($InputVector[2] -ge 2.45) {
        if ($InputVector[2] -ge 4.8500004) {
            $var3 = -0.14888482
        } else {
            $var3 = 0.2796613
        }
    } else {
        $var3 = -0.19143805
    }
    [double]$var4 = 0.0
    if ($InputVector[3] -ge 1.6500001) {
        $var4 = 0.40298507
    } else {
        if ($InputVector[2] -ge 4.95) {
            $var4 = 0.21724138
        } else {
            $var4 = -0.21974029
        }
    }
    [double]$var5 = 0.0
    if ($InputVector[2] -ge 4.75) {
        if ($InputVector[3] -ge 1.75) {
            $var5 = 0.28692952
        } else {
            $var5 = 0.06272897
        }
    } else {
        if ($InputVector[3] -ge 1.55) {
            $var5 = 0.009899145
        } else {
            $var5 = -0.19659369
        }
    }
    return Softmax $(@($(0.5 + ($var0 + $var1)), $(0.5 + ($var2 + $var3)), $(0.5 + ($var4 + $var5))))
}
function Softmax([double[]] $x) {
    [int] $size = $x.Length
    [double[]] $result = @(0) * $size
    [double] $max = $x[0]
    for ([int] $i = 1; $i -lt $size; ++$i) {
        if ($x[$i] -gt $max) {
            $max = $x[$i]
        }
    }
    [double] $sum = 0.0
    for ([int] $i = 0; $i -lt $size; ++$i) {
        $result[$i] = [math]::Exp($x[$i] - $max)
        $sum += $result[$i]
    }
    for ([int] $i = 0; $i -lt $size; ++$i) {
        $result[$i] /= $sum;
    }
    return $result
}
