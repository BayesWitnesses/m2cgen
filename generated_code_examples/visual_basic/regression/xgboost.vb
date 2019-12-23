Module Model
Function score(ByRef input_vector() As Double) As Double
    Dim var0 As Double
    If (input_vector(12)) >= (9.72500038) Then
        If (input_vector(12)) >= (16.0849991) Then
            var0 = 1.36374998
        Else
            var0 = 1.96335626
        End If
    Else
        If (input_vector(5)) >= (6.94099998) Then
            var0 = 3.74704218
        Else
            var0 = 2.48376822
        End If
    End If
    Dim var1 As Double
    If (input_vector(12)) >= (9.63000011) Then
        If (input_vector(12)) >= (19.2299995) Then
            var1 = 1.05852115
        Else
            var1 = 1.68638802
        End If
    Else
        If (input_vector(5)) >= (7.43700027) Then
            var1 = 3.95318961
        Else
            var1 = 2.40278864
        End If
    End If
    score = ((0.5) + (var0)) + (var1)
End Function
End Module
