Function Xatan(ByVal x As Double) As Double
    Dim z As Double
    z = x * x
    z = z * ((((-8.750608600031904122785e-01 * z _
                - 1.615753718733365076637e+01) * z _
               - 7.500855792314704667340e+01) * z _
              - 1.228866684490136173410e+02) * z _
             - 6.485021904942025371773e+01) _
        / (((((z + 2.485846490142306297962e+01) * z _
              + 1.650270098316988542046e+02) * z _
             + 4.328810604912902668951e+02) * z _
            + 4.853903996359136964868e+02) * z _
           + 1.945506571482613964425e+02)
    Xatan = x * z + x
End Function
Function Satan(ByVal x As Double) As Double
    Dim morebits as Double
    Dim tan3pio8 as Double
    morebits = 6.123233995736765886130e-17
    tan3pio8 = 2.41421356237309504880
    If x <= 0.66 Then
        Satan = Xatan(x)
        Exit Function
    End If
    If x > tan3pio8 Then
        Satan = 1.57079632679489661923132169163 - Xatan(1.0 / x) + morebits
        Exit Function
    End If
    Satan = 0.78539816339744830961566084581 + Xatan((x - 1) / (x + 1)) _
            + 3.061616997868382943065e-17
End Function
Function Atan(ByVal number As Double) As Double
    ' Implementation is taken from
    ' https://github.com/golang/go/blob/master/src/math/atan.go
    If number = 0.0 Then
        Atan = 0.0
        Exit Function
    End If
    If number > 0.0 Then
        Atan = Satan(number)
        Exit Function
    End If
    Atan = -Satan(-number)
End Function
