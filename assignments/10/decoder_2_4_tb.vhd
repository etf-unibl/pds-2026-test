-----------------------------------------------------------------------------
--
-- unit name:     decoder_2_4_tb
--
-- description:
--
--   Testbench for decoder 2 to 4 digital circuit
--
-----------------------------------------------------------------------------
-- The MIT License
-----------------------------------------------------------------------------
-- Copyright (c) 2026 Faculty of Electrical Engineering
--
-- Permission is hereby granted, free of charge, to any person obtaining a
-- copy of this software and associated documentation files (the "Software"),
-- to deal in the Software without restriction, including without limitation
-- the rights to use, copy, modify, merge, publish, distribute, sublicense,
-- and/or sell copies of the Software, and to permit persons to whom
-- the Software is furnished to do so, subject to the following conditions:
--
-- The above copyright notice and this permission notice shall be included in
-- all copies or substantial portions of the Software.
--
-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
-- IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
-- FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
-- THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
-- LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
-- ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
-- OTHER DEALINGS IN THE SOFTWARE
-----------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity decoder_2_4_tb is
end entity decoder_2_4_tb;

architecture arch of decoder_2_4_tb is

  signal a  : std_logic_vector(1 downto 0);
  signal en : std_logic;
  signal y  : std_logic_vector(3 downto 0);

  component decoder_2_4 is
    port (
      a_i  : in    std_logic_vector(1 downto 0);
      en_i : in    std_logic;
      y_o  : out   std_logic_vector(3 downto 0));
  end component decoder_2_4;

begin

  uut : component decoder_2_4
    port map (
      a_i  => a,
      en_i => en,
      y_o  => y);

  stimulus : process is
  begin

    for e in 0 to 1 loop

      for i in 0 to 3 loop

        a  <= std_logic_vector(to_unsigned(i, 2));
        en <= '1' when e = 1 else '0';
        wait for 10 ns;

        if e = 1 then
          assert y = std_logic_vector(shift_left(to_unsigned(1, 4), i))
            report "wrong output for a = " & integer'image(i)
            severity error;
        else
          assert y = "0000"
            report "output must be 0000 when disabled"
            severity error;
        end if;

      end loop;

    end loop;

    wait;

  end process stimulus;

end architecture arch;
