function Sigmoid([double] $x) {
    if ($x -lt 0.0) {
        [double] $z = [math]::Exp($x)
        return $z / (1.0 + $z)
    }
    return 1.0 / (1.0 + [math]::Exp(-$x))
}
