function softmax(x) result(res)
    implicit none
    double precision, dimension(:), intent(in) :: x
    double precision, dimension(size(x)) :: res
    double precision :: max_val, sum_val
    integer :: i

    ! Find maximum value in x
    max_val = x(1)
    do i = 2, size(x)
        if (x(i) > max_val) then
            max_val = x(i)
        end if
    end do

    ! Compute softmax values
    sum_val = 0.0d0
    do i = 1, size(x)
        res(i) = exp(x(i) - max_val)
        sum_val = sum_val + res(i)
    end do
    res = res / sum_val

end function softmax
