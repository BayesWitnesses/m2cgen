module Model
    implicit none
contains
    function score(input)
        implicit none
        double precision, dimension(:) :: input
        double precision, dimension(3) :: var0
        double precision, dimension(3) :: score
        if (input(3) <= 2.449999988079071d0) then
            var0 = (/ 1.0d0, 0.0d0, 0.0d0 /)
        else
            if (input(4) <= 1.75d0) then
                if (input(3) <= 4.950000047683716d0) then
                    if (input(4) <= 1.6500000357627869d0) then
                        var0 = (/ 0.0d0, 1.0d0, 0.0d0 /)
                    else
                        var0 = (/ 0.0d0, 0.0d0, 1.0d0 /)
                    end if
                else
                    var0 = (/ 0.0d0, 0.3333333333333333d0, 0.6666666666666666d0 /)
                end if
            else
                var0 = (/ 0.0d0, 0.021739130434782608d0, 0.9782608695652174d0 /)
            end if
        end if
        score(:) = var0
        return
    end function score
end module Model
