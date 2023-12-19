library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;

entity RV32I_System is
  Port (CLK, RST : in std_logic;
        A_Out, D_Out : out unsigned(31 downto 0));
end RV32I_System;

architecture Behavioral of RV32I_System is
    component RV32I is
        port(CLK, RST : in std_logic; -- clock and reset
             CS, WE : out std_logic; -- chip select and write enable for memory!
             ADDR, Data_OUT, PC_OUT : out unsigned(31 downto 0); -- address and data out for memory!
             Data_IN, Instruction_IN : in unsigned(31 downto 0)); -- data in from memory!
        end component;
    component Memory is
        port(CLK, CS, WE : in std_logic; -- Clock, chip select, and write enable
             SEL : in std_logic_vector(1 downto 0);
             ADDR, Data_IN, PC_IN : in unsigned(31 downto 0); -- address and data in (address size for this memory only consists of 9 bits)
             Instruction_OUT, Data_OUT : out unsigned(31 downto 0)); -- the output of the memory at ADDR
    end component;
    signal CS, WE : std_logic := '0';
    signal ADDR, Data_IN, Data_OUT, Instruction_IN, PC_OUT : unsigned(31 downto 0);
    signal SEL : std_logic_vector(1 downto 0);
begin
    CPU : RV32I port map(CLK => CLK,
                         RST => RST,
                         CS => CS,
                         WE => WE,
                         ADDR => ADDR,
                         Data_OUT => Data_OUT,
                         Data_IN => Data_IN,
                         Instruction_IN => Instruction_IN,
                         PC_OUT => PC_OUT);
                         
    MEM : Memory port map(CLK => CLK,
                          CS => CS,
                          WE => WE,
                          SEL => SEL,
                          ADDR => ADDR,
                          Data_IN => Data_OUT,
                          Data_OUT => Data_IN,
                          Instruction_Out => Instruction_IN,
                          PC_IN => PC_OUT);               

    A_Out <= ADDR;
    D_Out <= Data_Out;

end Behavioral;
