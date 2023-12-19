-- This file was specifically changed to a VHDL 2008 type. It is different in this way from other files in this project.

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;

-- This memory entity is designed to build the internal memory where programs are stored. Memory size is 1 kB which can hold 1024 instructions.
entity Memory is
  Port (CLK, CS, WE : in std_logic; -- Clock, chip select, and write enable
        SEL : in std_logic_vector(1 downto 0); -- Determine the data out and data in for byte, half word, and word
        ADDR, Data_IN, PC_IN : in unsigned(31 downto 0); -- address and data in (address size for this memory only consists of 9 bits)
        Instruction_OUT, Data_OUT : out unsigned(31 downto 0)); -- the output of the memory at ADDR
end Memory;

architecture Behavioral of Memory is
    type RAM is array (0 to 4092) of unsigned(7 downto 0); -- RAM type 4092 in size 8 bits wide for byte addressable memory (4KB)
    
    signal InstructionMemory : RAM := (others => (others => '0')); -- create the instruction memory and initialize all values to 0
    signal Instruction_Output, Data_Output, Data_Ext : unsigned(31 downto 0); -- Signal carrying the output value of default
    alias Data_BaseADDR : unsigned(7 downto 0) is Data_IN(7 downto 0);
    alias Data_Byte2 : unsigned(7 downto 0) is Data_IN(15 downto 8);
    alias Data_Byte3 : unsigned(7 downto 0) is Data_IN(23 downto 16);
    alias Data_Byte4 : unsigned(7 downto 0) is Data_IN(31 downto 24);

begin
    Instruction_OUT <= Instruction_Output; -- This is stating that Data_OUT must always output the "output" value
                                                                    -- irrespective of the clock (asynchronous); however, the output value
                                                                    -- is updated on the falling edge of the clock, making this a synchronous
                                                                    -- signal (in my opinion).    
    
    Data_OUT <= x"ZZZZZZZZ" when CS = '0' or WE = '1' else Data_Output;                                                                                                                                     
                                                                    
    process(CLK)
    begin
        if falling_edge(CLK) then
            if CS = '1' and WE = '1' then -- If the chip is selected AND the write enable is high, we would like to write a value to memory
                case SEL is
                    when "00" => -- word operation
                        if Data_BaseADDR <= 4088 then 
                            InstructionMemory(to_integer(ADDR(11 downto 0))) <= Data_BaseADDR;
                            InstructionMemory(to_integer(ADDR(11 downto 0))+1) <= Data_Byte2;
                            InstructionMemory(to_integer(ADDR(11 downto 0))+2) <= Data_Byte3;
                            InstructionMemory(to_integer(ADDR(11 downto 0))+3) <= Data_Byte4;
                        end if;    
                    when "01" => -- half word operation
                        if Data_BaseADDR <= 4090 then
                            InstructionMemory(to_integer(ADDR(11 downto 0))) <= Data_BaseADDR;
                            InstructionMemory(to_integer(ADDR(11 downto 0))+1) <= Data_Byte2;
                        end if;
                    when "10" => -- byte operation
                        if Data_BaseADDR <= 4092 then 
                            InstructionMemory(to_integer(ADDR(11 downto 0))) <= Data_BaseADDR;
                        end if;
                    when others =>
                end case;
            end if;
            Instruction_Output <= InstructionMemory(to_integer(PC_IN(11 downto 0))+3)
                                  &InstructionMemory(to_integer(PC_IN(11 downto 0))+2)
                                  &InstructionMemory(to_integer(PC_IN(11 downto 0))+1)
                                  &InstructionMemory(to_integer(PC_IN(11 downto 0))); -- Output the value of memory at address ADDR on every falling CLK
            
            case SEL is
                when "00" => -- word operation
                    if ADDR(11 downto 0) <= 4088 then
                        Data_Output <= InstructionMemory(to_integer(ADDR(11 downto 0))+3)
                                       &InstructionMemory(to_integer(ADDR(11 downto 0))+2)
                                       &InstructionMemory(to_integer(ADDR(11 downto 0))+1)
                                       &InstructionMemory(to_integer(ADDR(11 downto 0)));
                    end if;
                when "01" => -- half word operation
                    if ADDR(11 downto 0) <= 4090 then
                        Data_Output <= x"0000"
                                       &InstructionMemory(to_integer(ADDR(11 downto 0))+1)
                                       &InstructionMemory(to_integer(ADDR(11 downto 0)));
                    end if;                                 
                when "10" => -- byte operation
                    if ADDR(11 downto 0) <= 4092 then
                        Data_Output <= x"000000"
                                       &InstructionMemory(to_integer(ADDR(11 downto 0)));
                    end if;
                when others =>
            end case;
            
            
        end if;
    end process;                                                                  

end Behavioral;
