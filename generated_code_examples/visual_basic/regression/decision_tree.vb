Module Model
Function score(ByRef input_vector() As Double) As Double
    Dim var0 As Double
    If (input_vector(5)) <= (6.941) Then
        If (input_vector(12)) <= (14.4) Then
            If (input_vector(7)) <= (1.38485) Then
                var0 = 45.58
            Else
                var0 = 22.939004149377574
            End If
        Else
            var0 = 14.910404624277467
        End If
    Else
        If (input_vector(5)) <= (7.4370003) Then
            var0 = 32.11304347826088
        Else
            var0 = 45.096666666666664
        End If
    End If
    score = var0
End Function
End Module
