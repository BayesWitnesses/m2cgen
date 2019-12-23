Module Model
Function score(ByRef input_vector() As Double) As Double
    Dim var0 As Double
    If (input_vector(12)) <= (8.91) Then
        If (input_vector(5)) <= (6.902) Then
            If (input_vector(7)) <= (1.48495) Then
                var0 = 50.0
            Else
                var0 = 25.320000000000004
            End If
        Else
            var0 = 38.34810126582279
        End If
    Else
        If (input_vector(0)) <= (5.84803) Then
            var0 = 19.99185520361991
        Else
            var0 = 12.102469135802467
        End If
    End If
    Dim var1 As Double
    If (input_vector(12)) <= (9.725) Then
        If (input_vector(5)) <= (7.4525) Then
            If (input_vector(5)) <= (6.7539997) Then
                var1 = 24.801739130434775
            Else
                var1 = 32.47230769230769
            End If
        Else
            var1 = 47.075
        End If
    Else
        If (input_vector(12)) <= (15.0) Then
            var1 = 20.44094488188976
        Else
            var1 = 14.823214285714291
        End If
    End If
    score = ((var0) * (0.5)) + ((var1) * (0.5))
End Function
End Module
