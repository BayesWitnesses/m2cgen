Module Model
Function score(ByRef input_vector() As Double) As Double()
    Dim var0(2) As Double
    var0(0) = ((((9.774126241420623) + ((input_vector(0)) * (-0.41545978008486634))) + ((input_vector(1)) * (0.9619661444337051))) + ((input_vector(2)) * (-2.5028461157608604))) + ((input_vector(3)) * (-1.0766107732916166))
    var0(1) = ((((2.248771246116064) + ((input_vector(0)) * (0.5239098915475155))) + ((input_vector(1)) * (-0.3177027667958222))) + ((input_vector(2)) * (-0.20333498652290763))) + ((input_vector(3)) * (-0.9399605394445277))
    var0(2) = ((((-12.022897487538232) + ((input_vector(0)) * (-0.10845011146263966))) + ((input_vector(1)) * (-0.6442633776378855))) + ((input_vector(2)) * (2.7061811022837774))) + ((input_vector(3)) * (2.01657131273614))
    score = var0
End Function
End Module
