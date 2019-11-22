Module Model
Function score(ByRef input_vector() As Double) As Double
    Dim var0 As Double
    If (input_vector(5)) <= (6.941) Then
        If (input_vector(12)) <= (14.395) Then
            If (input_vector(7)) <= (1.43365) Then
                var0 = 45.58
            Else
                var0 = 22.865022421524642
            End If
        Else
            var0 = 14.924358974358983
        End If
    Else
        If (input_vector(5)) <= (7.4370003) Then
            var0 = 32.09534883720931
        Else
            var0 = 45.275
        End If
    End If
    score = var0
End Function
End Module
