Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    If inputVector(12) <= 9.845000267028809 Then
        If inputVector(5) <= 6.959500074386597 Then
            If inputVector(6) <= 96.20000076293945 Then
                var0 = 25.093162393162395
            Else
                var0 = 50.0
            End If
        Else
            var0 = 38.074999999999996
        End If
    Else
        If inputVector(12) <= 15.074999809265137 Then
            var0 = 20.518439716312056
        Else
            var0 = 14.451282051282046
        End If
    End If
    Dim var1 As Double
    If inputVector(12) <= 9.650000095367432 Then
        If inputVector(5) <= 7.437000036239624 Then
            If inputVector(7) <= 1.47284996509552 Then
                var1 = 50.0
            Else
                var1 = 26.7965317919075
            End If
        Else
            var1 = 44.21176470588236
        End If
    Else
        If inputVector(12) <= 17.980000495910645 Then
            var1 = 19.645652173913035
        Else
            var1 = 12.791919191919195
        End If
    End If
    Score = (var0 + var1) * 0.5
End Function
End Module
