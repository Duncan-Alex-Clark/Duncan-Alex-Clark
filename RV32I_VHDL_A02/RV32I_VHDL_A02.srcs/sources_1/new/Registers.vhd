library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;

-- This register entity is designed to consist of 32 general purpose registers which are 32 bits wide
entity REG is
    port(CLK : in std_logic; -- Including a CLK is what makes this sychronous
         WE : in std_logic; -- Write Enable
         RegA, RegB, RegC : in unsigned(4 downto 0); -- 2 Source registers and a destination register. 5 bit addressing allows for 32 registers, so obviously these are the addressing bits.
         DW : in unsigned(31 downto 0); -- Data Write, data to be written when write enable is high
         DataA, DataB : out unsigned(31 downto 0)); -- Data stored at registers A & B, output is asynchronous.
end REG;

architecture Behavioral of REG is
    type RAM is array (0 to 31) of unsigned(31 downto 0); -- Declaring a RAM type which has 32 itterations of a 32 bit unsigned size. 
    
    signal Registers : RAM := (others => (others => '0')); -- Initialize all the registers to have a value of 0.
    alias zero : unsigned is Registers(0);
    alias ra : unsigned is Registers(1);
    alias sp : unsigned is Registers(2);
    alias gp : unsigned is Registers(3);
    alias tp : unsigned is Registers(4);
    alias t0 : unsigned is Registers(5);
    alias t1 : unsigned is Registers(6);
    alias t2 : unsigned is Registers(7);
    alias s0_fp : unsigned is Registers(8);
    alias s1 : unsigned is Registers(9);
    alias a0 : unsigned is Registers(10);
    alias a1 : unsigned is Registers(11);
    alias a2 : unsigned is Registers(12);
    alias a3 : unsigned is Registers(13);
    alias a4 : unsigned is Registers(14);
    alias a5 : unsigned is Registers(15);
    alias a6 : unsigned is Registers(16);
    alias a7 : unsigned is Registers(17);
    alias s2 : unsigned is Registers(18);
    alias s3 : unsigned is Registers(19);
    alias s4 : unsigned is Registers(20);
    alias s5 : unsigned is Registers(21);
    alias s6 : unsigned is Registers(22);
    alias s7 : unsigned is Registers(23);
    alias s8 : unsigned is Registers(24);
    alias s9 : unsigned is Registers(25);
    alias s10 : unsigned is Registers(26);
    alias s11 : unsigned is Registers(27);
    alias t3 : unsigned is Registers(28);
    alias t4 : unsigned is Registers(29);
    alias t5 : unsigned is Registers(30);
    alias t6 : unsigned is Registers(31);
    
    
begin
    process(CLK)
    begin
        if rising_edge(CLK) then
            if WE = '1' and RegC /= 0 then -- Register 0 is hardwired to 0. When RegC isn't 0 and WE is 1, write the data the register.
                Registers(to_integer(RegC)) <= DW; -- Write the data to register
            end if;
        end if;
    end process;
    
    DataA <= Registers(to_integer(RegA)); -- DataA should output the value stored at RegA at all times (asynchronous)
    DataB <= Registers(to_integer(RegB)); -- DataB should output the value stored at RegB at all times (asynchronous)

end Behavioral;
