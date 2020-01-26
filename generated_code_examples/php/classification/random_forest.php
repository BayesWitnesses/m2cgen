<?php
function add_vectors(array $v1, array $v2) {
    $result = array();
    for ($i = 0; $i < count($v1); ++$i) {
        $result[] = $v1[$i] + $v2[$i];
    }
    return $result;
}
function mul_vector_number(array $v1, $num) {
    $result = array();
    for ($i = 0; $i < count($v1); ++$i) {
        $result[] = $v1[$i] * $num;
    }
    return $result;
}
function score(array $input) {
    $var0 = array();
    if (($input[3]) <= (0.8)) {
        $var0 = array(1.0, 0.0, 0.0);
    } else {
        if (($input[2]) <= (4.8500004)) {
            $var0 = array(0.0, 0.9622641509433962, 0.03773584905660377);
        } else {
            if (($input[3]) <= (1.75)) {
                if (($input[3]) <= (1.6500001)) {
                    $var0 = array(0.0, 0.25, 0.75);
                } else {
                    $var0 = array(0.0, 1.0, 0.0);
                }
            } else {
                $var0 = array(0.0, 0.0, 1.0);
            }
        }
    }
    $var1 = array();
    if (($input[3]) <= (0.8)) {
        $var1 = array(1.0, 0.0, 0.0);
    } else {
        if (($input[0]) <= (6.1499996)) {
            if (($input[2]) <= (4.8500004)) {
                $var1 = array(0.0, 0.9090909090909091, 0.09090909090909091);
            } else {
                $var1 = array(0.0, 0.0, 1.0);
            }
        } else {
            if (($input[3]) <= (1.75)) {
                $var1 = array(0.0, 0.8666666666666667, 0.13333333333333333);
            } else {
                $var1 = array(0.0, 0.0, 1.0);
            }
        }
    }
    return add_vectors(mul_vector_number($var0, 0.5), mul_vector_number($var1, 0.5));
}
