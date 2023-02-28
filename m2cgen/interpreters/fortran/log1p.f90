function ChebyshevBroucke(x, coeffs) result(result)
    implicit none
    double precision, intent(in) :: x
    double precision, intent(in) :: coeffs(:)
    double precision :: b0, b1, b2, x2, result
    integer :: i
    b2 = 0.0d0
    b1 = 0.0d0
    b0 = 0.0d0
    x2 = x * 2.0d0
    do i = size(coeffs, 1), 1, -1
        b2 = b1
        b1 = b0
        b0 = x2 * b1 - b2 + coeffs(i)
    end do
    result = (b0 - b2) * 0.5d0
end function ChebyshevBroucke

function Log1p(x) result(result)
    implicit none
    double precision, intent(in) :: x
    double precision :: res, xAbs
    double precision, parameter :: eps = 2.220446049250313d-16
    double precision, parameter :: coeff(21) = (/ 0.10378693562743769800686267719098d1, &
            -0.13364301504908918098766041553133d0, &
            0.19408249135520563357926199374750d-1, &
            -0.30107551127535777690376537776592d-2, &
            0.48694614797154850090456366509137d-3, &
            -0.81054881893175356066809943008622d-4, &
            0.13778847799559524782938251496059d-4, &
            -0.23802210894358970251369992914935d-5, &
            0.41640416213865183476391859901989d-6, &
            -0.73595828378075994984266837031998d-7, &
            0.13117611876241674949152294345011d-7, &
            -0.23546709317742425136696092330175d-8, &
            0.42522773276034997775638052962567d-9, &
            -0.77190894134840796826108107493300d-10, &
            0.14075746481359069909215356472191d-10, &
            -0.25769072058024680627537078627584d-11, &
            0.47342406666294421849154395005938d-12, &
            -0.87249012674742641745301263292675d-13, &
            0.16124614902740551465739833119115d-13, &
            -0.29875652015665773006710792416815d-14, &
            0.55480701209082887983041321697279d-15, &
            -0.10324619158271569595141333961932d-15 /)

    if (x == 0.0d0) then
        result = 0.0d0
        return
    end if
    if (x == -1.0d0) then
        result = -huge(1.0d0)
        return
    end if
    if (x < -1.0) then
        result = 0.0d0 / 0.0d0
        return
    end if

    xAbs = abs(x)
    if (xAbs < 0.5 * eps) then
        result = x
        return
    end if

    if ((x > 0.0 .and. x < 1.0e-8) .or. (x > -1.0e-9 .and. x < 0.0)) then
        result = x * (1.0 - x * 0.5)
        return
    end if

    if (xAbs < 0.375) then
        result = x * (1.0 - x * ChebyshevBroucke(x / 0.375, coeff))
        return
    end if

    result = log(1.0 + x)

end function Log1p

