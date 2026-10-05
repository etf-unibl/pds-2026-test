-----------------------------------------------------------------------------
--
-- unit name:     four_bit_comparator
--
-- description:
--
--   This file implements a simple four_bit_comparator logic.
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

entity four_bit_comparator is
  port (
    a_i    : in    std_logic_vector(3 downto 0);
    b_i    : in    std_logic_vector(3 downto 0);
    agtb_o : out   std_logic;
    aeqb_o : out   std_logic;
    altb_o : out   std_logic);
end entity four_bit_comparator;

architecture arch of four_bit_comparator is

  component two_bit_comparator is
    port (
      a_i    : in    std_logic_vector(1 downto 0);
      b_i    : in    std_logic_vector(1 downto 0);
      agtb_o : out   std_logic;
      aeqb_o : out   std_logic;
      altb_o : out   std_logic);
  end component two_bit_comparator;

  signal hi_gt : std_logic;
  signal hi_eq : std_logic;
  signal hi_lt : std_logic;
  signal lo_gt : std_logic;
  signal lo_eq : std_logic;
  signal lo_lt : std_logic;

begin

  hi : component two_bit_comparator
    port map (
      a_i    => a_i(3 downto 2),
      b_i    => b_i(3 downto 2),
      agtb_o => hi_gt,
      aeqb_o => hi_eq,
      altb_o => hi_lt);

  lo : component two_bit_comparator
    port map (
      a_i    => a_i(1 downto 0),
      b_i    => b_i(1 downto 0),
      agtb_o => lo_gt,
      aeqb_o => lo_eq,
      altb_o => lo_lt);

  agtb_o <= hi_gt or (hi_eq and lo_gt);
  aeqb_o <= hi_eq and lo_eq;
  altb_o <= hi_lt or (hi_eq and lo_lt);

end architecture arch;
