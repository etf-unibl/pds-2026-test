-----------------------------------------------------------------------------
--
-- unit name:     four_bit_comparator
--
-- description:
--
--   This file implements a comparator of two 4-bit unsigned numbers built
--   structurally from two 2-bit comparators.
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

--! @file
--! @brief Comparator of two 4-bit unsigned numbers

library ieee;
use ieee.std_logic_1164.all;

--! @brief Comparator of two 4-bit unsigned numbers
--! @details Compares the unsigned numbers a_i and b_i. Exactly one of the
--! outputs agtb_o, aeqb_o and altb_o is '1' at any time. The circuit is
--! purely combinational.
--! @see two_bit_comparator

entity four_bit_comparator is
  port (
    a_i    : in    std_logic_vector(3 downto 0); --! First number (unsigned)
    b_i    : in    std_logic_vector(3 downto 0); --! Second number (unsigned)
    agtb_o : out   std_logic;                    --! '1' when a_i > b_i
    aeqb_o : out   std_logic;                    --! '1' when a_i = b_i
    altb_o : out   std_logic);                   --! '1' when a_i < b_i
end entity four_bit_comparator;

--! @brief Structural architecture of the 4-bit comparator
--! @details Two 2-bit comparators compare the higher (bits 3..2) and the
--! lower (bits 1..0) bit pairs. The higher pair decides the result; the
--! lower pair is used only when the higher pairs are equal.

architecture arch of four_bit_comparator is

  --! Comparator of two 2-bit unsigned numbers
  component two_bit_comparator is
    port (
      a_i    : in    std_logic_vector(1 downto 0);
      b_i    : in    std_logic_vector(1 downto 0);
      agtb_o : out   std_logic;
      aeqb_o : out   std_logic;
      altb_o : out   std_logic);
  end component two_bit_comparator;

  signal hi_gt : std_logic; --! Higher bit pair of a_i is greater
  signal hi_eq : std_logic; --! Higher bit pairs are equal
  signal hi_lt : std_logic; --! Higher bit pair of a_i is less
  signal lo_gt : std_logic; --! Lower bit pair of a_i is greater
  signal lo_eq : std_logic; --! Lower bit pairs are equal
  signal lo_lt : std_logic; --! Lower bit pair of a_i is less

begin

  --! Comparator of the higher bit pair (bits 3..2)
  hi : component two_bit_comparator
    port map (
      a_i    => a_i(3 downto 2),
      b_i    => b_i(3 downto 2),
      agtb_o => hi_gt,
      aeqb_o => hi_eq,
      altb_o => hi_lt);

  --! Comparator of the lower bit pair (bits 1..0)
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
