module Model
    implicit none
contains
    function score(input)
        implicit none
        double precision, dimension(:) :: input
        double precision :: var0
        double precision :: var1
        double precision :: var2
        double precision :: var3
        double precision :: var4
        double precision :: var5
        double precision, dimension(3) :: score
        if (input(3) >= 2.45d0) then
            var0 = -0.21995015d0
        else
            var0 = 0.4302439d0
        end if
        if (input(3) >= 2.45d0) then
            var1 = -0.19691855d0
        else
            var1 = 0.29493433d0
        end if
        if (input(3) >= 2.45d0) then
            if (input(4) >= 1.75d0) then
                var2 = -0.20051816d0
            else
                var2 = 0.36912444d0
            end if
        else
            var2 = -0.21512198d0
        end if
        if (input(3) >= 2.45d0) then
            if (input(3) >= 4.8500004d0) then
                var3 = -0.14888482d0
            else
                var3 = 0.2796613d0
            end if
        else
            var3 = -0.19143805d0
        end if
        if (input(4) >= 1.6500001d0) then
            var4 = 0.40298507d0
        else
            if (input(3) >= 4.95d0) then
                var4 = 0.21724138d0
            else
                var4 = -0.21974029d0
            end if
        end if
        if (input(3) >= 4.75d0) then
            if (input(4) >= 1.75d0) then
                var5 = 0.28692952d0
            else
                var5 = 0.06272897d0
            end if
        else
            if (input(4) >= 1.55d0) then
                var5 = 0.009899145d0
            else
                var5 = -0.19659369d0
            end if
        end if
        score(:) = SOFTMAX((/ 0.5d0 + var0 + var1, 0.5d0 + var2 + var3, 0.5d0 + var4 + var5 /))
        return
    end function score
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
end module Model
