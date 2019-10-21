function Score([double[]] $InputVector) {
    [double]$var0 = 0
    if (($InputVector[5]) -gt (6.8455)) {
        if (($InputVector[5]) -gt (7.437)) {
            $var0 = 24.906664851995615
        } else {
            $var0 = 23.513674700555555
        }
    } else {
        if (($InputVector[12]) -gt (14.395000000000001)) {
            $var0 = 21.863487452747595
        } else {
            $var0 = 22.70305627629392
        }
    }
    [double]$var1 = 0
    if (($InputVector[12]) -gt (9.63)) {
        if (($InputVector[12]) -gt (19.830000000000002)) {
            $var1 = -0.9644646678713786
        } else {
            $var1 = -0.30629733662250097
        }
    } else {
        if (($InputVector[5]) -gt (7.437)) {
            $var1 = 2.0368334157126293
        } else {
            $var1 = 0.4576204330349962
        }
    }
    return ((0) + ($var0)) + ($var1)
}
