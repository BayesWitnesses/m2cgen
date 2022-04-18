function Score([double[]] $InputVector) {
    [double[]]$var0 = @(0.0)
    if ($InputVector[2] -le 2.449999988079071) {
        $var0 = @($(1.0), $(0.0), $(0.0))
    } else {
        if ($InputVector[3] -le 1.75) {
            if ($InputVector[2] -le 4.950000047683716) {
                if ($InputVector[3] -le 1.6500000357627869) {
                    $var0 = @($(0.0), $(1.0), $(0.0))
                } else {
                    $var0 = @($(0.0), $(0.0), $(1.0))
                }
            } else {
                $var0 = @($(0.0), $(0.3333333333333333), $(0.6666666666666666))
            }
        } else {
            $var0 = @($(0.0), $(0.021739130434782608), $(0.9782608695652174))
        }
    }
    return $var0
}
