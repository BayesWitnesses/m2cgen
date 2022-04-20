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
            cond do read(input,12) >= 9.725 ->
                cond do read(input,12) >= 19.23 ->
                    3.5343752
                true ->
                    5.5722494
                end
            true ->
                cond do read(input,5) >= 6.941 ->
                    11.1947155
                true ->
                    7.4582143
                end
            end
        end
        func1 = fn ->
            cond do read(input,12) >= 5.1549997 ->
                cond do read(input,12) >= 15.0 ->
                    2.8350503
                true ->
                    4.8024607
                end
            true ->
                cond do read(input,5) >= 7.406 ->
                    10.0011215
                true ->
                    6.787523
                end
            end
        end
        0.5 + (func0.() + func1.())
    end
end
