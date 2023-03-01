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
        if (input(3) > 3.1500000000000004d0) then
            var0 = -1.1986122886681099d0
        else
            if (input(2) > 3.35d0) then
                var0 = -0.8986122886681098d0
            else
                var0 = -0.9136122886681098d0
            end if
        end if
        if (input(3) > 3.1500000000000004d0) then
            if (input(3) > 4.450000000000001d0) then
                var1 = -0.09503010837903424d0
            else
                var1 = -0.09563272415214283d0
            end if
        else
            if (input(2) > 3.35d0) then
                var1 = 0.16640323607832397d0
            else
                var1 = 0.15374604217339707d0
            end if
        end if
        if (input(3) > 1.8d0) then
            if (input(4) > 1.6500000000000001d0) then
                var2 = -1.2055899476674514d0
            else
                var2 = -0.9500445227622534d0
            end if
        else
            var2 = -1.2182214705715104d0
        end if
        if (input(4) > 0.45000000000000007d0) then
            if (input(4) > 1.6500000000000001d0) then
                var3 = -0.08146437273923739d0
            else
                var3 = 0.14244886188108738d0
            end if
        else
            if (input(3) > 1.4500000000000002d0) then
                var3 = -0.0950888159264695d0
            else
                var3 = -0.09438233722389686d0
            end if
        end if
        if (input(4) > 1.6500000000000001d0) then
            if (input(3) > 5.3500000000000005d0) then
                var4 = -0.8824095771015287d0
            else
                var4 = -0.9121126703829481d0
            end if
        else
            if (input(3) > 4.450000000000001d0) then
                var4 = -1.1277829563828181d0
            else
                var4 = -1.1794405099157212d0
            end if
        end if
        if (input(3) > 4.750000000000001d0) then
            if (input(3) > 5.150000000000001d0) then
                var5 = 0.16625543464258166d0
            else
                var5 = 0.09608601737074281d0
            end if
        else
            if (input(1) > 4.950000000000001d0) then
                var5 = -0.09644547407948921d0
            else
                var5 = -0.08181864271444342d0
            end if
        end if
        score(:) = SOFTMAX((/ var0 + var1, var2 + var3, var4 + var5 /))
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
