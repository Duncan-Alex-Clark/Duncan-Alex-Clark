-- The following program is influenced heavily by the MIPS program from ECE 441. 

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.all;

entity RV32I is
  port (CLK, RST : in std_logic; -- clock and reset
        CS, WE : out std_logic; -- chip select and write enable for memory!
        SEL : out std_logic_vector(1 downto 0);
        ADDR, Data_OUT, PC_OUT : out unsigned(31 downto 0); -- address and data out for memory!
        Data_IN, Instruction_IN : in unsigned(31 downto 0)); -- data in from memory!
end RV32I;

architecture Behavioral of RV32I is
    -- Within the processor core fabric exists the registers, and so, they are instantiated here. This is opposed to instruction memory which, in this model, is external to the core.
    component REG is
        port(CLK : in std_logic; -- Including a CLK is what makes this sychronous
             WE : in std_logic; -- Write Enable
             RegA, RegB, RegC : in unsigned(4 downto 0); -- 2 Source registers and a destination register. 5 bit addressing allows for 32 registers, so obviously these are the addressing bits.
             DW : in unsigned(31 downto 0); -- Data Write, data to be written when write enable is high
             DataA, DataB : out unsigned(31 downto 0)); -- Data stored at registers A & B, output is asynchronous.
    end component;
    
    -- below are the list of operations which can be performed by the RV32I core
    type operation is (LUI,
                       AUIPC,
                       JAL,
                       JALR,
                       BEQ,
                       BNE,
                       BLT,
                       BGE,
                       BLTU,
                       BGEU,
                       LB, -- Instruction tested and working
                       LH, -- Instruction tested and working
                       LW, -- Instruction tested and working
                       LBU, -- Instruction tested and working
                       LHU, -- Instruction tested and working
                       SB,
                       SH,
                       SW,
                       ADDI, -- Instruction tested and working
                       SLTI, -- Instruction tested and working
                       SLTIU, -- Instruction tested and working
                       XORI, -- Instruction tested and working
                       ORI, -- Instruction tested and working
                       ANDI, -- Instruction tested and working
                       SLLI, -- Instruction tested and working
                       SRLI, -- Instruction tested and working
                       SRAI, -- Instruction tested and working
                       ADD, -- Instruction tested and working
                       SUB, -- Instruction tested and working
                       SLL_R, -- 
                       SLT,
                       SLTU,
                       XOR_R, -- 
                       SRL_R, -- 
                       SRA_R, -- 
                       OR_R, -- 
                       AND_R, -- 
                       FENCE, -- not implemented at this time
                       ECALL, -- not implemented at this time
                       EBREAK -- not implemented at this time
                         );
    
    type InstructionType is (R, I, S, B, U, J); -- All instruction encoding formats
    
    signal Op : Operation;
    signal SEL_save : std_logic_vector(1 downto 0) := "00";
    signal Format : InstructionType;
    
    signal State, nState : integer range 0 to 4 := 0;
    signal RegWE, MEM_Reading : std_logic; -- CPU status and control signals 
    signal RegA, RegB, RegC : unsigned(4 downto 0);
    signal DW, DataA, DataB, Data_IN_Ext : unsigned(31 downto 0);   
    signal PC, nPC : unsigned(31 downto 0) := x"00000000";
    signal ALU_A, ALU_B, ALU_Result, Imm_Ext : unsigned(31 downto 0) := x"ZZZZZZZZ";
    signal Instruction : unsigned(31 downto 0) := x"ZZZZZZZZ";
    signal imm_I : unsigned(11 downto 0);
    signal imm_S : unsigned(11 downto 0);
    signal imm_B : unsigned(12 downto 1); -- 12 bits encoded in instruction, bit 0 is always 0
    signal imm_U : unsigned(31 downto 12); 
    signal imm_J : unsigned(20 downto 1); -- 20 bits encoded in instruction, bit 0 is always 0
    alias opcode : unsigned(6 downto 0) is Instruction(6 downto 0);
    alias funct3 : unsigned(2 downto 0) is Instruction(14 downto 12); 
    alias funct7 : unsigned(6 downto 0) is Instruction(31 downto 25); 
    alias rs1 : unsigned(4 downto 0) is Instruction(19 downto 15); 
    alias rs2 : unsigned(4 downto 0) is Instruction(24 downto 20);
    alias rd : unsigned(4 downto 0) is Instruction(11 downto 7);
                             
                         
                         
                         
begin
-- Create an instance of the 32 general purpose registers
    GP_Registers : REG 
        port map(CLK => CLK, 
                 WE => RegWE, 
                 RegA => RegA, 
                 RegB => RegB, 
                 RegC => RegC, 
                 DW => DW, 
                 DataA => DataA, 
                 DataB => DataB); 
                 
-- Immediate value signal assignments for decoding (would like to make these aliases in the future)
    imm_I <= Instruction(31 downto 20);
    imm_S <= Instruction(31 downto 25)
             &Instruction(11 downto 7);
    imm_B <= Instruction(31) -- imm(12)
             &Instruction(7) -- imm(11)
             &Instruction(30 downto 25) -- imm(10 downto 5)
             &Instruction(11 downto 8); -- imm(4 downto 1)
     imm_U <= Instruction(31 downto 12);
     imm_J <= Instruction(31) -- imm(20)
              &Instruction(19 downto 12) -- imm(19 downto 12)
              &Instruction(20) -- imm(11)
              &Instruction(30 downto 21); -- imm(10 downto 1)
              
-- Immediate extensions for each decoded immediate type
    Immediate_Extension : process(CLK, Format, imm_I, imm_S, imm_B, imm_U, imm_J)
    begin
        case Format is
            when I =>
                Imm_Ext <= x"FFFFF" & imm_I when imm_I(11) = '1'
                           else x"00000" & imm_I;
            when S =>
                Imm_Ext <= x"FFFFF" & imm_S when imm_S(11) = '1'
                           else x"00000" & imm_S;
            when B =>
                Imm_Ext <= x"FFF" & "1111111" & imm_B & '0' when imm_B(12) = '1'
                           else x"000" & "0000000" & imm_B & '0';
            when U =>
                Imm_Ext <= imm_U & x"000";
            when J =>
                Imm_Ext <= x"FF" & "111" & imm_J & '0' when imm_J(20) = '1'
                           else x"00" & "000" & imm_J & '0';
            when others =>
        end case;
    end process;
    
    -- Data coming into the core from memory must be sign extended when the instruction requires. Otherwise,
    -- the incoming data can remain unchanged.
    Data_IN_Extension : process(CLK, Data_IN, SEL)
    begin
        if Op = LB or Op = LH or Op = LW then
            case SEL is
                when "01" =>
                   Data_IN_Ext <= x"FFFF"
                                  &Data_IN(15 downto 0) when Data_IN(15) = '1' 
                             else x"0000"
                                  &Data_IN(15 downto 0);
                when "10" =>
                    Data_IN_Ext <= x"FFFFFF"
                                  &Data_IN(7 downto 0) when Data_IN(7) = '1' 
                             else x"000000"
                                  &Data_IN(7 downto 0);
                when others =>
            end case;
        else
            Data_IN_Ext <= Data_IN;
        end if;
    end process;
    
    -- Decode the instruction and deterime the instruction format
    Format <= R when opcode = "0110011"
         else I when opcode = "1100111" or opcode = "0000011" or opcode = "0010011"
         else S when opcode = "0100011"
         else B when opcode = "1100011"
         else U when opcode = "0110111" or opcode = "0010111"
         else J when opcode = "1101111";
    
    ADDR <= x"ZZZZZZZZ" when MEM_reading = '0' else ALU_Result; -- ADDR is driven to high impedance when memory is not being read, else ALU_Result
    PC_OUT <= PC; -- Attach the internal PC to the PC_OUT port
    ALU_A <= PC when Op = JAL
             --else Data_IN when MEM_reading = '1'
             else DataA; -- The A input of the ALU is connected the the DataA output of the Register component
    ALU_B <= DataB when Format = R or Format = S or Format = B
             else Imm_Ext when Format = I or Format = U or Format = J;
    Data_OUT <= DataB when WE = '1' else x"ZZZZZZZZ"; -- Data to be written to memory is equal to DataB register output when writing to memory
    -- These may need to be multiplexed but at this moment I'm not sure
    RegA <= rs1;
    RegB <= rs2;
    RegC <= rd;
    DW <= nPC when Op = JAL or Op = JALR
          else Data_IN_Ext when MEM_reading = '1'
          else ALU_Result;
    
    -- Control Signals
    
    SEL <= SEL_save;
    
    CPU_Execution_Cycle : process(State, Instruction, funct3, PC, Format, Op, ALU_A, ALU_B)
    begin  
        -- Initialize status and control signals to 0
        CS <= '0';
        RegWE <= '0';
        case State is
            when 0 => -- Instruction fetch
                nState <= 1; -- Progress to the next state
                nPC <= PC + 4; -- Increment the program counter
                CS <= '1'; -- Enable the CS pin to allow for memory operation
                SEL_save <= "00";
                WE <= '0';
                MEM_Reading <= '0';
            when 1 => -- Instruction decode
            -- Instruction decode is performed after the instruction is fetched from memory. The instruction is comprised of many parts
            -- which all have a destination depending on the type of instruction. The purpose of the decode stage is to route all 
            -- components of the instruction where they need to go within the CPU.
                nState <= 2;
                case Format is
                    when R =>
                        if funct7 = "0000000" then
                            case funct3 is
                                when "000" => Op <= ADD;
                                when "001" => Op <= SLL_R;
                                when "010" => Op <= SLT;
                                when "011" => Op <= SLTU;
                                when "100" => Op <= XOR_R;
                                when "101" => Op <= SRL_R;
                                when "110" => Op <= OR_R;
                                when "111" => Op <= AND_R;
                                when others =>
                            end case;   
                        else
                            case funct3 is
                                when "000" => Op <= SUB;
                                when "101" => Op <= SRA_R;
                                when others =>
                            end case;
                        end if;
                    when I =>
                        if opcode = "1100111" then Op <= JALR; 
                        elsif opcode = "0000011" then
                            case funct3 is
                                when "000" => 
                                    Op <= LB;
                                    SEL_save <= "10";
                                when "001" => 
                                    Op <= LH;
                                    SEL_save <= "01";
                                when "010" => Op <= LW;
                                when "100" => 
                                    Op <= LBU;
                                    SEL_save <= "10";
                                when "101" => 
                                    Op <= LHU;
                                    SEL_save <= "01";
                                when others =>
                            end case;
                        else
                            if funct7 = "0000000" and funct3 = "101" then Op <= SRLI; end if;
                            if funct7 = "0100000" and funct3 = "101" then Op <= SRAI; end if;  
                            case funct3 is
                                when "000" => Op <= ADDI;
                                when "010" => Op <= SLTI;
                                when "011" => Op <= SLTIU;
                                when "100" => Op <= XORI;
                                when "110" => Op <= ORI;
                                when "111" => Op <= ANDI;
                                when "001" => Op <= SLLI;   
                                when others =>
                            end case;
                        end if;
                    when S =>
                        case funct3 is
                            when "000" => 
                                Op <= SB;
                                SEL_save <= "10";
                            when "001" => 
                                Op <= SH;
                                SEL_save <= "01";
                            when "010" => Op <= SW;
                            when others =>
                        end case;
                    when B =>
                        case funct3 is
                            when "000" => Op <= BEQ;
                            when "001" => Op <= BNE;
                            when "100" => Op <= BLT;
                            when "101" => Op <= BGE;
                            when "110" => Op <= BLTU;
                            when "111" => Op <= BGEU;
                            when others =>
                        end case;
                    when U =>
                        if opcode = "0110111" then Op <= LUI; 
                        else Op <= AUIPC; 
                        end if;
                    when J =>
                        Op <= JAL;
                    when others =>
                end case;
            when 2 => -- Instruction execute
                nState <= 0;
                RegWE <= '1' when Format = R or Format = I or Format = U or Format = J
                         else '0';
                case Op is
                    when LUI => ALU_Result <= ALU_B;
                    when AUIPC => ALU_Result <= unsigned(signed(PC) + signed(ALU_B));
                    when JAL => ALU_Result <= unsigned(signed(ALU_A) + signed(ALU_B));
                    when JALR => ALU_Result <= unsigned(signed(ALU_A) + signed(ALU_B));
                    when BEQ => ALU_Result <= unsigned(signed(ALU_A) + signed(ALU_B));
                    when BNE => ALU_Result <= unsigned(signed(ALU_A) + signed(ALU_B));
                    when BLT => ALU_Result <= unsigned(signed(ALU_A) + signed(ALU_B));
                    when BGE => ALU_Result <= unsigned(signed(ALU_A) + signed(ALU_B));
                    when BLTU => ALU_Result <= unsigned(signed(ALU_A) + signed(ALU_B));
                    when BGEU => ALU_Result <= unsigned(signed(ALU_A) + signed(ALU_B));
                    when LB => MEM_Reading <= '1';
                        MEM_Reading <= '1'; RegWE <= '0'; nState <= 3;
                        ALU_Result <= to_unsigned((to_integer(ALU_A)) + (to_integer(Imm_Ext)), 32);
                    when LH => 
                        MEM_Reading <= '1'; RegWE <= '0'; nState <= 3;
                        ALU_Result <= to_unsigned((to_integer(ALU_A)) + (to_integer(Imm_Ext)), 32);
                    when LW => 
                        MEM_Reading <= '1'; RegWE <= '0'; nState <= 3;
                        ALU_Result <= to_unsigned((to_integer(ALU_A)) + (to_integer(Imm_Ext)), 32);
                    when LBU => 
                        MEM_Reading <= '1'; RegWE <= '0'; nState <= 3;
                        ALU_Result <= to_unsigned((to_integer(ALU_A)) + (to_integer(Imm_Ext)), 32);
                    when LHU => 
                        MEM_Reading <= '1'; RegWE <= '0'; nState <= 3;
                        ALU_Result <= to_unsigned((to_integer(ALU_A)) + (to_integer(Imm_Ext)), 32);
                    when SB => WE <= '1';
                    when SH => WE <= '1';
                    when SW => WE <= '1';
                    when ADDI => ALU_Result <= unsigned(signed(ALU_A) + signed(ALU_B));
                    when SLTI => ALU_Result <= x"00000001" when signed(ALU_A) < signed(ALU_B) else x"00000000"; 
                    when SLTIU => ALU_Result <= x"00000001" when ALU_A < ALU_B else x"00000000";
                    when XORI => ALU_Result <= ALU_A xor ALU_B;
                    when ORI =>  ALU_Result <= ALU_A or ALU_B;
                    when ANDI => ALU_Result <= ALU_A and ALU_B;
                    when SLLI => ALU_Result <= ALU_A sll to_integer(Instruction(24 downto 20));
                    when SRLI => ALU_Result <= ALU_A srl to_integer(Instruction(24 downto 20));
                    when SRAI => ALU_Result <= unsigned(signed(ALU_A) sra to_integer(Instruction(24 downto 20)));
                    when ADD => ALU_Result <= unsigned(signed(ALU_A) + signed(ALU_B));
                    when SUB => ALU_Result <= unsigned(signed(ALU_A) - signed(ALU_B));
                    when SLL_R => ALU_Result <= unsigned(signed(ALU_A) + signed(ALU_B));
                    when SLT => ALU_Result <= x"00000001" when signed(ALU_A) < signed(ALU_B) else x"00000000";
                    when SLTU => ALU_Result <= x"00000001" when ALU_A < ALU_B else x"00000000";
                    when XOR_R => ALU_Result <= ALU_A xor ALU_B;
                    when SRL_R => ALU_Result <= ALU_A srl to_integer(rs2);
                    when SRA_R => ALU_Result <= ALU_A sra to_integer(rs2);
                    when OR_R => ALU_Result <= ALU_A or ALU_B;
                    when AND_R => ALU_Result <= ALU_A and ALU_B;
                    when others =>
                end case;
            when 3 => -- Memory access
            if MEM_Reading = '1' and WE = '0' then CS <= '1'; RegWE <= '1'; nState <= 0;
            elsif MEM_Reading = '1' or WE = '1' then CS <= '1'; nState <= 4;
            else nState <= 0;
            end if;
            when 4 => -- Write register
            WE <= '1';
            nState <= 0;
            CS <= '1';
            when others =>
        end case;
    end process;
    
    Synchronize_CPU : process(CLK)
    begin
        if rising_edge(CLK) then
            if RST = '1' then -- The reset signal for the processor is high
                State <= 0; -- Set the state to 0
                PC <= x"00000000"; -- Set the program counter to 0
            else
                State <= nState;
                PC <= nPC;
--                PC <= ALU_Result when Op <= JAL or Op = JALR 
--                      or (Op = BEQ and rs1 = rs2)
--                      or (Op = BNE and rs1 /= rs2)
--                      or (Op = BLT and signed(rs1) < signed(rs2))
--                      or (Op = BGE and signed(rs1) >= signed(rs2))
--                      or (Op = BLTU and unsigned(rs1) < unsigned(rs2))
--                      or (Op = BGEU and unsigned(rs1) >= unsigned(rs2))
--                      else nPC;
            end if;
            if State = 0 then Instruction <= Instruction_IN; end if; -- state 0 is the fetch state
            --if state = 3 and MEM_Reading = '1' then MEM_Reading <= '1'; end if; 
        end if;
    end process;
    


end Behavioral;
