Function AddVectors(ByRef v1() As Double, ByRef v2() As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) + v2(i)
    Next i

    AddVectors = result
End Function
Function MulVectorNumber(ByRef v1() As Double, ByVal num As Double) As Double()
    Dim resLength As Integer
    resLength = UBound(v1) - LBound(v1)
    Dim result() As Double
    ReDim result(resLength)

    Dim i As Integer
    For i = LBound(v1) To UBound(v1)
        result(i) = v1(i) * num
    Next i

    MulVectorNumber = result
End Function
