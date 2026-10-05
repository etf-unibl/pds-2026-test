-----------------------------------------------------------------------------
--
-- unit name:     two_bit_comparator
--
-- description:
--
--   This file implements a simple two_bit_comparator logic.
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

entity two_bit_comparator is
  port (
    i_a    : in    std_logic_vector(1 downto 0);
    i_b    : in    std_logic_vector(1 downto 0);
    o_agtb : out   std_logic;
    o_aeqb : out   std_logic;
    o_altb : out   std_logic);
end entity two_bit_comparator;

architecture arch of two_bit_comparator is

  signal eq : std_logic;
  signal gt : std_logic;

begin

  eq     <= (i_a(1) xnor i_b(1)) and (i_a(0) xnor i_b(0));
  gt     <= (i_a(1) and not i_b(1)) or ((i_a(1) xnor i_b(1)) and i_a(0) and not i_b(0));
  o_aeqb <= eq;
  o_agtb <= gt;
  o_altb <= not (eq or gt);

end architecture arch;
