<?php
function score(array $input) {
    $var0 = null;
    if (($input[2]) >= (2.45000005)) {
        $var0 = -0.0733167157;
    } else {
        $var0 = 0.143414631;
    }
    $var1 = null;
    if (($input[2]) >= (2.45000005)) {
        $var1 = -0.0706516728;
    } else {
        $var1 = 0.125176534;
    }
    $var2 = null;
    $var2 = exp(((0.5) + ($var0)) + ($var1));
    $var3 = null;
    if (($input[2]) >= (2.45000005)) {
        if (($input[3]) >= (1.75)) {
            $var3 = -0.0668393895;
        } else {
            $var3 = 0.123041473;
        }
    } else {
        $var3 = -0.0717073306;
    }
    $var4 = null;
    if (($input[2]) >= (2.45000005)) {
        if (($input[3]) >= (1.75)) {
            $var4 = -0.0642274022;
        } else {
            $var4 = 0.10819874;
        }
    } else {
        $var4 = -0.069036141;
    }
    $var5 = null;
    $var5 = exp(((0.5) + ($var3)) + ($var4));
    $var6 = null;
    if (($input[3]) >= (1.6500001)) {
        $var6 = 0.13432835;
    } else {
        if (($input[2]) >= (4.94999981)) {
            $var6 = 0.0724137947;
        } else {
            $var6 = -0.0732467622;
        }
    }
    $var7 = null;
    if (($input[3]) >= (1.6500001)) {
        $var7 = 0.117797568;
    } else {
        if (($input[2]) >= (4.94999981)) {
            $var7 = 0.0702545047;
        } else {
            $var7 = -0.0706570372;
        }
    }
    $var8 = null;
    $var8 = exp(((0.5) + ($var6)) + ($var7));
    $var9 = null;
    $var9 = (($var2) + ($var5)) + ($var8);
    return array(($var2) / ($var9), ($var5) / ($var9), ($var8) / ($var9));
}
