Module Model
Function Score(ByRef inputVector() As Double) As Double
    Dim var0 As Double
    If inputVector(12) <= 9.724999904632568 Then
        If inputVector(5) <= 7.437000036239624 Then
            If inputVector(7) <= 1.4849499464035034 Then
                var0 = 50.0
            Else
                var0 = 26.681034482758605
            End If
        Else
            var0 = 44.96896551724139
        End If
    Else
        If inputVector(12) <= 16.085000038146973 Then
            var0 = 20.284353741496595
        Else
            var0 = 14.187142857142863
        End If
    End If
    Score = var0
End Function
End Module
