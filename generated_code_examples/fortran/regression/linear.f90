module Model
    implicit none
contains
    function score(input)
        implicit none
        double precision, dimension(:) :: input

        double precision :: score
        score = 36.367080746577244d0 + input(1) * -0.10861311354908008d0 + input(2) * 0.046461486329936456d0 + input(3) * 0.027432259970172148d0 + input(4) * 2.6160671309537777d0 + input(5) * -17.51793656329737d0 + input(6) * 3.7674418196772255d0 + input(7) * -0.000021581753164971046d0 + input(8) * -1.4711768622633645d0 + input(9) * 0.2956767140062958d0 + input(10) * -0.012233831527259383d0 + input(11) * -0.9220356453705304d0 + input(12) * 0.009038220462695552d0 + input(13) * -0.542583033714222d0
        return
    end function score
end module Model
