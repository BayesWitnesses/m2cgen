function sigmoid(x) result(res)
    implicit none
    double precision, intent(in) :: x
    double precision :: z

    if (x < 0.0d0) then
        z = exp(x)
        res = z / (1.0d0 + z)
    else
        res = 1.0d0 / (1.0d0 + exp(-x))
    end if

end function sigmoid
