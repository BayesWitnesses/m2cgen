Function Tanh(ByVal number As Double) As Double
    ' Implementation is taken from
    ' https://github.com/golang/go/blob/master/src/math/tanh.go
    Dim z As Double
    z = Math.Abs(number)
    If z > 44.0148459655565271479942397125 Then
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
        * ((-0.964399179425052238628 * s + -99.2877231001918586564) * s + -1614.68768441708447952) _
        / (((s + 112.811678491632931402) * s + 2235.48839060100448583) * s + 4844.06305325125486048)
    Tanh = z
End Function
