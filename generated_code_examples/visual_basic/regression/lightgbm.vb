Module Model
Function score(ByRef input_vector() As Double) As Double
    Dim var0 As Double
    If (input_vector(5)) > (6.918000000000001) Then
        If (input_vector(5)) > (7.437) Then
            var0 = 24.81112131071211
        Else
            var0 = 23.5010290754961
        End If
    Else
        If (input_vector(12)) > (14.365) Then
            var0 = 21.796569516771488
        Else
            var0 = 22.640634908349323
        End If
    End If
    Dim var1 As Double
    If (input_vector(12)) > (9.63) Then
        If (input_vector(12)) > (19.23) Then
            var1 = -0.9218520876020193
        Else
            var1 = -0.30490175606373926
        End If
    Else
        If (input_vector(5)) > (7.437) Then
            var1 = 2.028554553190867
        Else
            var1 = 0.45970642160364367
        End If
    End If
    score = ((0) + (var0)) + (var1)
End Function
End Module
