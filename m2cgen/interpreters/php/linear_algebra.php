function addVectors(array $v1, array $v2) {
    $result = array();
    for ($i = 0; $i < count($v1); ++$i) {
        $result[] = $v1[$i] + $v2[$i];
    }
    return $result;
}
function mulVectorNumber(array $v1, $num) {
    $result = array();
    for ($i = 0; $i < count($v1); ++$i) {
        $result[] = $v1[$i] * $num;
    }
    return $result;
}
