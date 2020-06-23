Function Tanh(ByVal number As Double) As Double
    ' Implementation is taken from
    ' https://github.com/golang/go/blob/master/src/math/tanh.go
    Dim z As Double
    z = Math.Abs(number)
    If z > 0.440148459655565271479942397125e+2 Then
        If number < 0 Then
            Tanh = -1.0
            Exit Function
        End If
        Tanh = 1.0
        Exit Function
    End If
    If z >= 0.625 Then
        z = 1 - 2 / (Math.Exp(2 * z) + 1)
        If number < 0 Then
            z = -z
        End If
        Tanh = z
        Exit Function
    End If
    If number = 0 Then
        Tanh = 0.0
        Exit Function
    End If
    Dim s As Double
    s = number * number
    z = number + number * s _
        * ((-0.964399179425052238628e+0 * s + -0.992877231001918586564e+2) _
           * s + -0.161468768441708447952e+4) _
        / (((s + 0.112811678491632931402e+3) _
            * s + 0.223548839060100448583e+4) _
           * s + 0.484406305325125486048e+4)
    Tanh = z
End Function
