module Model
    implicit none
contains
    function score(input)
        implicit none
        double precision, dimension(:) :: input
        double precision, dimension(3) :: var0
        double precision, dimension(3) :: var1
        double precision, dimension(3) :: score
        if (input(4) <= 0.75d0) then
            var0 = (/ 1.0d0, 0.0d0, 0.0d0 /)
        else
            if (input(3) <= 4.75d0) then
                var0 = (/ 0.0d0, 1.0d0, 0.0d0 /)
            else
                if (input(3) <= 5.049999952316284d0) then
                    if (input(4) <= 1.75d0) then
                        var0 = (/ 0.0d0, 0.8333333333333334d0, 0.16666666666666666d0 /)
                    else
                        var0 = (/ 0.0d0, 0.08333333333333333d0, 0.9166666666666666d0 /)
                    end if
                else
                    var0 = (/ 0.0d0, 0.0d0, 1.0d0 /)
                end if
            end if
        end if
        if (input(4) <= 0.800000011920929d0) then
            var1 = (/ 1.0d0, 0.0d0, 0.0d0 /)
        else
            if (input(1) <= 6.25d0) then
                if (input(3) <= 4.8500001430511475d0) then
                    var1 = (/ 0.0d0, 0.9487179487179487d0, 0.05128205128205128d0 /)
                else
                    var1 = (/ 0.0d0, 0.0d0, 1.0d0 /)
                end if
            else
                if (input(4) <= 1.550000011920929d0) then
                    var1 = (/ 0.0d0, 0.8333333333333334d0, 0.16666666666666666d0 /)
                else
                    var1 = (/ 0.0d0, 0.02564102564102564d0, 0.9743589743589743d0 /)
                end if
            end if
        end if
        score(:) = mul_vector_number(add_vectors(var0, var1), 0.5d0)
        return
    end function score
    function add_vectors(v1, v2) result(res)
        implicit none
        double precision, dimension(:), intent(in) :: v1, v2
        double precision, dimension(size(v1)) :: res
        integer :: i

        do i = 1, size(v1)
            res(i) = v1(i) + v2(i)
        end do

    end function add_vectors

    function mul_vector_number(v1, num) result(res)
        implicit none
        double precision, dimension(:), intent(in) :: v1
        double precision, intent(in) :: num
        double precision, dimension(size(v1)) :: res
        integer :: i

        do i = 1, size(v1)
            res(i) = v1(i) * num
        end do

    end function mul_vector_number
end module Model
