defmodule Model do
    @compile {:inline, read: 2}
    defp read(bin, pos) do
        <<_::size(pos)-unit(64)-binary, value::float, _::binary>> = bin
        value
    end
    defp list_to_binary(list) do
        for i <- list, into: <<>>, do: <<i::float>>
    end
    def score(input) do
        input = list_to_binary(input)
        func0 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.1 - read(input,0), 2.0) + :math.pow(2.5 - read(input,1), 2.0) + :math.pow(3.0 - read(input,2), 2.0) + :math.pow(1.1 - read(input,3), 2.0)))
        end
        func1 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(4.9 - read(input,0), 2.0) + :math.pow(2.4 - read(input,1), 2.0) + :math.pow(3.3 - read(input,2), 2.0) + :math.pow(1.0 - read(input,3), 2.0)))
        end
        func2 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(6.3 - read(input,0), 2.0) + :math.pow(2.5 - read(input,1), 2.0) + :math.pow(4.9 - read(input,2), 2.0) + :math.pow(1.5 - read(input,3), 2.0)))
        end
        func3 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.4 - read(input,0), 2.0) + :math.pow(3.0 - read(input,1), 2.0) + :math.pow(4.5 - read(input,2), 2.0) + :math.pow(1.5 - read(input,3), 2.0)))
        end
        func4 = fn ->
            0.11172510039290856 + func0.() * -0.8898986041811555 + func1.() * -0.8898986041811555 + func2.() * -0.0 + func3.() * -0.0
        end
        func5 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(6.2 - read(input,0), 2.0) + :math.pow(2.2 - read(input,1), 2.0) + :math.pow(4.5 - read(input,2), 2.0) + :math.pow(1.5 - read(input,3), 2.0)))
        end
        func6 = fn ->
            func5.() * -0.0
        end
        func7 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.6 - read(input,0), 2.0) + :math.pow(2.9 - read(input,1), 2.0) + :math.pow(3.6 - read(input,2), 2.0) + :math.pow(1.3 - read(input,3), 2.0)))
        end
        func8 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(6.7 - read(input,0), 2.0) + :math.pow(3.0 - read(input,1), 2.0) + :math.pow(5.0 - read(input,2), 2.0) + :math.pow(1.7 - read(input,3), 2.0)))
        end
        func9 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.0 - read(input,0), 2.0) + :math.pow(2.3 - read(input,1), 2.0) + :math.pow(3.3 - read(input,2), 2.0) + :math.pow(1.0 - read(input,3), 2.0)))
        end
        func10 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(6.0 - read(input,0), 2.0) + :math.pow(2.7 - read(input,1), 2.0) + :math.pow(5.1 - read(input,2), 2.0) + :math.pow(1.6 - read(input,3), 2.0)))
        end
        func11 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.9 - read(input,0), 2.0) + :math.pow(3.2 - read(input,1), 2.0) + :math.pow(4.8 - read(input,2), 2.0) + :math.pow(1.8 - read(input,3), 2.0)))
        end
        func12 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.7 - read(input,0), 2.0) + :math.pow(2.6 - read(input,1), 2.0) + :math.pow(3.5 - read(input,2), 2.0) + :math.pow(1.0 - read(input,3), 2.0)))
        end
        func13 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.0 - read(input,0), 2.0) + :math.pow(3.0 - read(input,1), 2.0) + :math.pow(1.6 - read(input,2), 2.0) + :math.pow(0.2 - read(input,3), 2.0)))
        end
        func14 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.4 - read(input,0), 2.0) + :math.pow(3.4 - read(input,1), 2.0) + :math.pow(1.7 - read(input,2), 2.0) + :math.pow(0.2 - read(input,3), 2.0)))
        end
        func15 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.7 - read(input,0), 2.0) + :math.pow(3.8 - read(input,1), 2.0) + :math.pow(1.7 - read(input,2), 2.0) + :math.pow(0.3 - read(input,3), 2.0)))
        end
        func16 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(4.8 - read(input,0), 2.0) + :math.pow(3.4 - read(input,1), 2.0) + :math.pow(1.9 - read(input,2), 2.0) + :math.pow(0.2 - read(input,3), 2.0)))
        end
        func17 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(4.5 - read(input,0), 2.0) + :math.pow(2.3 - read(input,1), 2.0) + :math.pow(1.3 - read(input,2), 2.0) + :math.pow(0.3 - read(input,3), 2.0)))
        end
        func18 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.7 - read(input,0), 2.0) + :math.pow(4.4 - read(input,1), 2.0) + :math.pow(1.5 - read(input,2), 2.0) + :math.pow(0.4 - read(input,3), 2.0)))
        end
        func19 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.1 - read(input,0), 2.0) + :math.pow(3.8 - read(input,1), 2.0) + :math.pow(1.9 - read(input,2), 2.0) + :math.pow(0.4 - read(input,3), 2.0)))
        end
        func20 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.1 - read(input,0), 2.0) + :math.pow(3.3 - read(input,1), 2.0) + :math.pow(1.7 - read(input,2), 2.0) + :math.pow(0.5 - read(input,3), 2.0)))
        end
        func21 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(6.2 - read(input,0), 2.0) + :math.pow(2.8 - read(input,1), 2.0) + :math.pow(4.8 - read(input,2), 2.0) + :math.pow(1.8 - read(input,3), 2.0)))
        end
        func22 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(7.2 - read(input,0), 2.0) + :math.pow(3.0 - read(input,1), 2.0) + :math.pow(5.8 - read(input,2), 2.0) + :math.pow(1.6 - read(input,3), 2.0)))
        end
        func23 = fn ->
            -0.04261957451303831 + func21.() * -0.37953658977037247 + func22.() * -0.0
        end
        func24 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(6.1 - read(input,0), 2.0) + :math.pow(3.0 - read(input,1), 2.0) + :math.pow(4.9 - read(input,2), 2.0) + :math.pow(1.8 - read(input,3), 2.0)))
        end
        func25 = fn ->
            func24.() * -0.0
        end
        func26 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(6.0 - read(input,0), 2.0) + :math.pow(3.0 - read(input,1), 2.0) + :math.pow(4.8 - read(input,2), 2.0) + :math.pow(1.8 - read(input,3), 2.0)))
        end
        func27 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(4.9 - read(input,0), 2.0) + :math.pow(2.5 - read(input,1), 2.0) + :math.pow(4.5 - read(input,2), 2.0) + :math.pow(1.7 - read(input,3), 2.0)))
        end
        func28 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(7.9 - read(input,0), 2.0) + :math.pow(3.8 - read(input,1), 2.0) + :math.pow(6.4 - read(input,2), 2.0) + :math.pow(2.0 - read(input,3), 2.0)))
        end
        func29 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(5.6 - read(input,0), 2.0) + :math.pow(2.8 - read(input,1), 2.0) + :math.pow(4.9 - read(input,2), 2.0) + :math.pow(2.0 - read(input,3), 2.0)))
        end
        func30 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(6.0 - read(input,0), 2.0) + :math.pow(2.2 - read(input,1), 2.0) + :math.pow(5.0 - read(input,2), 2.0) + :math.pow(1.5 - read(input,3), 2.0)))
        end
        func31 = fn ->
            :math.exp(-0.06389634699048878 * (:math.pow(6.3 - read(input,0), 2.0) + :math.pow(2.8 - read(input,1), 2.0) + :math.pow(5.1 - read(input,2), 2.0) + :math.pow(1.5 - read(input,3), 2.0)))
        end
        func32 = fn ->
            1.8136162062461285 + func21.() * -110.34516826676301 + func22.() * -13.999391039896215 + func24.() * -108.44329471899991 + func26.() * -110.34516826676301 + func27.() * -22.21095753342801
        end
        func33 = fn ->
            func28.() * -0.0
        end
        [func4.() + func6.() + func7.() * -0.756413813553974 + func8.() * -0.0 + func9.() * -0.8898986041811555 + func10.() * -0.0 + func11.() * -0.0 + func12.() * -0.8898986041811555 + func13.() * 0.04218875216876044 + func14.() * 0.7142250613852136 + func15.() * 0.0 + func16.() * 0.8898986041811555 + func17.() * 0.8898986041811555 + func18.() * 0.0 + func19.() * 0.8898986041811555 + func20.() * 0.8898986041811555, func23.() + func25.() + func26.() * -0.37953658977037247 + func27.() * -0.37953658977037247 + func28.() * -0.26472396872040066 + func29.() * -0.3745962010653211 + func30.() * -0.10077618026650095 + func31.() * -0.0 + func13.() * 0.0 + func14.() * 0.0 + func15.() * 0.37953658977037247 + func16.() * 0.37953658977037247 + func17.() * 0.3044555865539922 + func18.() * 0.05610417372785803 + func19.() * 0.37953658977037247 + func20.() * 0.37953658977037247, func32.() + func33.() + func29.() * -0.0 + func30.() * -65.00217641452454 + func31.() * -110.34516826676301 + func0.() * 0.0 + func1.() * 0.0 + func2.() * 110.34516826676301 + func3.() * 62.115561183470184 + func5.() * 37.19509025661546 + func7.() * 0.0 + func8.() * 110.34516826676301 + func9.() * 0.0 + func10.() * 110.34516826676301 + func11.() * 110.34516826676301 + func12.() * 0.0]
    end
end
