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
        [9.700311953536998 + read(input,0) * -0.4128360473754751 + read(input,1) * 0.9680426131053453 + read(input,2) * -2.498310603183548 + read(input,3) * -1.0723230787022542, 2.1575759475871163 + read(input,0) * 0.5400806228605453 + read(input,1) * -0.3245383349519669 + read(input,2) * -0.2034493200950831 + read(input,3) * -0.9338183426196143, -11.857887901124615 + read(input,0) * -0.12724457548509432 + read(input,1) * -0.6435042781533917 + read(input,2) * 2.7017599232786216 + read(input,3) * 2.006141421321863]
    end
end
