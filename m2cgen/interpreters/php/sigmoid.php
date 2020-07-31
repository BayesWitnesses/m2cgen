function sigmoid($x) {
    if ($x < 0.0) {
        $z = exp($x);
        return $z / (1.0 + $z);
    }
    return 1.0 / (1.0 + exp(-$x));
}
