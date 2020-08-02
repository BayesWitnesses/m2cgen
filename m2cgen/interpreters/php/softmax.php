function softmax(array $x) {
    $size = count($x);
    $result = array();
    $m = max($x);
    $sum = 0.0;
    for ($i = 0; $i < $size; ++$i) {
        $result[$i] = exp($x[$i] - $m);
        $sum += $result[$i];
    }
    for ($i = 0; $i < $size; ++$i) {
        $result[$i] /= $sum;
    }
    return $result;
}
