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
        36.367080746577244 + read(input,0) * -0.10861311354908008 + read(input,1) * 0.046461486329936456 + read(input,2) * 0.027432259970172148 + read(input,3) * 2.6160671309537777 + read(input,4) * -17.51793656329737 + read(input,5) * 3.7674418196772255 + read(input,6) * -0.000021581753164971046 + read(input,7) * -1.4711768622633645 + read(input,8) * 0.2956767140062958 + read(input,9) * -0.012233831527259383 + read(input,10) * -0.9220356453705304 + read(input,11) * 0.009038220462695552 + read(input,12) * -0.542583033714222
    end
end
