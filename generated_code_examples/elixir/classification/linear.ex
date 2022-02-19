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
        [((((9.70057332319769) + ((read(input,0)) * (-0.41301996479716235))) + ((read(input,1)) * (0.968278235077753))) + ((read(input,2)) * (-2.498251993123262))) + ((read(input,3)) * (-1.0723281263725812)), ((((2.1581957283451367) + ((read(input,0)) * (0.540053774261645))) + ((read(input,1)) * (-0.32455711571440043))) + ((read(input,2)) * (-0.2034786488926118))) + ((read(input,3)) * (-0.9339902405677639)), ((((-11.858769051542865) + ((read(input,0)) * (-0.12703380946447623))) + ((read(input,1)) * (-0.6437211193633476))) + ((read(input,2)) * (2.701730642015882))) + ((read(input,3)) * (2.0063183669403477))]
    end
end
