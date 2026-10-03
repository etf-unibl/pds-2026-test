-----------------------------------------------------------------------------
--
-- unit name:     TEST
--
-- description:
--
--   Test design for the submission procedure (NAND gate).
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
--! @brief Two-input NAND gate

library ieee;
use ieee.std_logic_1164.all;

--! @brief Two-input NAND gate
--! @details The output is the inverted logical AND of the two inputs.

entity test is
  port (
    a_i : in    std_logic;  --! First input
    b_i : in    std_logic;  --! Second input
    y_o : out   std_logic); --! Output, not (a_i and b_i)
end entity test;

--! @brief Dataflow architecture of the NAND gate
--! @details A single concurrent signal assignment.

architecture arch of test is

begin

  y_o <= a_i nand b_i;

end architecture arch;
