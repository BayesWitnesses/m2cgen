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
