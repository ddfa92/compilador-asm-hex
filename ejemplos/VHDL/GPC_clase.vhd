library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;

entity GPC_clase is
    Port ( clk      : in  STD_LOGIC;
           rst      : in  STD_LOGIC;
			  enter	  : in  STD_LOGIC;
           Din		  : in  STD_LOGIC_VECTOR (15 downto 0);
			  Dout	  : out STD_LOGIC_VECTOR (15 downto 0);
           inFlags  : out STD_LOGIC_VECTOR (7 downto 0);
           outFlags : out STD_LOGIC_VECTOR (7 downto 0);
			  done     : out STD_LOGIC);          
end GPC_clase;

architecture Behavioral of GPC_clase is

------------- COMPONENT Declaration ------ COMP_TAG
component ramBlock
	port (
	addr: IN std_logic_VECTOR(7 downto 0);
	clk:  IN std_logic;
	din:  IN std_logic_VECTOR(15 downto 0);
	dout: OUT std_logic_VECTOR(15 downto 0);
	we:   IN std_logic);
end component;

-- Synplicity black box declaration
attribute syn_black_box : boolean;
attribute syn_black_box of ramBlock: component is true;

-- COMP_TAG_END ------ End COMPONENT Declaration ------------

-- registers ------------------------------------------------
signal IR:unsigned (15 downto 0);    --instrucciones: 16 bits 
signal PC:unsigned (7 downto 0);     --12 bits: maximo tamaño de memoria 4096 bytes
signal SP:unsigned (7 downto 0);     --12 bits: maximo tamaño de la pila (stack) 4096 bytes
signal AC:signed   (15 downto 0);    --ISA: acumulador de 16 bits

signal AUX:unsigned (15 downto 0);
signal TMP:unsigned (7 downto 0);

signal aux_inFlags:unsigned (7 downto 0);
signal aux_outFlags:unsigned (7 downto 0);

type state_t is(fetch,fetch_a,fetch_b,decode,LODD,LODD_a,LODD_b,STOD,STOD_a,STOD_b,ADDD,ADDD_a,ADDD_b,SUBD,SUBD_a,SUBD_b,JPOS,JZER,JUMP,LOCO,LODL,LODL_a,LODL_b,STOL,STOL_a,STOL_b,ADDL,ADDL_a,ADDL_b,SUBL,SUBL_a,SUBL_b,
                JNEG,JNZE,CALL,CALL_a,CALL_b,CALL_c,PUSHI,PUSHI_a,PUSHI_b,PUSHI_c,PUSHI_d,PUSHI_e,PUSHI_f,POPI,POPI_a,POPI_b,POPI_c,POPI_d,POPI_e,PUSH,PUSH_a,PUSH_b,PUSH_c,POP,POP_a,POP_b,RETN,SWAP,SWAP_a,INSP,DESP,INPAC,OUTAC,HALT);
signal state:state_t;

signal ramAddr:std_logic_vector(7 downto 0);	
signal ramDin,ramDout:std_logic_vector(15 downto 0);	
signal ramWE:std_logic;	

begin
------------- INSTANTIATION Template ----- INST_TAG
myram : ramBlock
		port map (
			addr => ramAddr,
			clk  => clk,
			din  => ramDin,
			dout => ramDout,
			we   => ramWE);
-- INST_TAG_END ------ End INSTANTIATION Template ------------

                          
	process(clk,rst)
		variable I : integer range 0 to 3;
   begin
		if rst='1'then
			state<=fetch;
			PC<=x"00";  -- start of RAM
			SP<=x"FF";  -- end of RAM
			AC<=(others=>'0');	
			Dout<=(others=>'0');  
         inFlags <=(others=>'0');			
			aux_inFlags <="00000001";
			outFlags <=(others=>'0');
			aux_outFlags <="00000001";			
			done<='0';
			ramWE<='0';
		elsif rising_edge(clk) then
			case state is
			
				--fetch
				when fetch   => ramAddr <= std_logic_vector(PC);state<=fetch_a;		   
				when fetch_a => state<=fetch_b;
				when fetch_b => IR<= unsigned(ramDout);PC<=PC+1;state<=decode;
               
				--decode
				when decode => 
					CASE IR(15 DOWNTO 12) IS -- decode first 8 bits of IR as opcode and memory addressing
						WHEN X"0" => state <= LODD;
						WHEN X"1" => state <= STOD;
						WHEN X"2" => state <= ADDD;
						WHEN X"3" => state <= SUBD;
						WHEN X"4" => state <= JPOS;
						WHEN X"5" => state <= JZER;
						WHEN X"6" => state <= JUMP;
						WHEN X"7" => state <= LOCO;
						WHEN X"8" => state <= LODL;
						WHEN X"9" => state <= STOL;
						WHEN X"A" => state <= ADDL;
						WHEN X"B" => state <= SUBL;
						WHEN X"C" => state <= JNEG;
						WHEN X"D" => state <= JNZE;
						WHEN X"E" => state <= CALL;
						WHEN X"F" => 
							case IR(11 DOWNTO 8) is
								when X"0" => state <= PUSHI;
								when X"1" => state <= POPI;
								when X"2" => state <= PUSH;
								when X"3" => state <= POP;
								when X"4" => state <= RETN;
								when X"5" => state <= SWAP;
								when X"6" => state <= INSP;
								when X"7" => state <= DESP;
								when X"8" => state <= INPAC;
								when X"9" => state <= OUTAC;
								when X"A" => state <= HALT;						
							   WHEN OTHERS => NULL;		
							end case;
						WHEN OTHERS => NULL;
					END CASE;	
					
				--execute:
				--LODD
				when LODD   => ramAddr <= std_logic_vector(IR(7 downto 0));state<=LODD_a;			     
				when LODD_a =>	state<=LODD_b;
				when LODD_b => AC <= signed(ramDout);state<=fetch;	
							
				--STOD
				when STOD   => ramAddr <= std_logic_vector(IR(7 downto 0));state<=STOD_a;		
				when STOD_a =>	ramDin<= std_logic_vector(AC);ramWE<='1';state<=STOD_b;
				when STOD_b =>	ramWE<='0';state<=fetch;
												
            --ADDD	
            when ADDD   => ramAddr <= std_logic_vector(IR(7 downto 0));state<=ADDD_a;	
            when ADDD_a =>	state<=ADDD_b;
				when ADDD_b => AC <= AC + signed(ramDout);state<=fetch;

            --SUBD	
            when SUBD   => ramAddr <= std_logic_vector(IR(7 downto 0));state<=SUBD_a;	
            when SUBD_a =>	state<=SUBD_b;
				when SUBD_b => AC <= AC - signed(ramDout);state<=fetch;

				--JPOS	
				when JPOS =>	
					if AC>=0 then 
						PC<=IR(7 downto 0);
					end if;	
					state<=fetch;	
					
				--JZER	
				when JZER =>	
					if AC=0 then 
						PC<=IR(7 downto 0);
					end if;	
					state<=fetch;	
					
				--JUMP	
				when JUMP => PC<=IR(7 downto 0);state<=fetch;		
					
				--LOCO
				when LOCO => AC<=signed(x"0"&IR(11 downto 0));state<=fetch;
				  	
				--LODL	
				when LODL   => ramAddr <= std_logic_vector(SP+IR(7 downto 0));state<=LODL_a;			     
				when LODL_a =>	state<=LODL_b;
				when LODL_b => AC <= signed(ramDout);state<=fetch;	
					
				--STOL
				when STOL   => ramAddr <= std_logic_vector(SP+IR(7 downto 0));state<=STOL_a;		
				when STOL_a =>	ramDin<= std_logic_vector(AC);ramWE<='1';state<=STOL_b;
				when STOL_b =>	ramWE<='0';state<=fetch;

            --ADDL	
            when ADDL   => ramAddr <= std_logic_vector(SP+IR(7 downto 0));state<=ADDL_a;	
            when ADDL_a =>	state<=ADDL_b;
				when ADDL_b => AC <= AC + signed(ramDout);state<=fetch;

            --SUBL	
            when SUBL   => ramAddr <= std_logic_vector(SP+IR(7 downto 0));state<=SUBL_a;	
            when SUBL_a =>	state<=SUBL_b;
				when SUBL_b => AC <= AC - signed(ramDout);state<=fetch;

				--JNEG
				when JNEG =>	
					if AC<0 then 
						PC<=IR(7 downto 0);
					end if;	
					state<=fetch;	
					
				--JZER	
				when JNZE =>	
					if AC/=0 then 
						PC<=IR(7 downto 0);
					end if;	
					state<=fetch;	
					
            --CALL					
            when CALL   => SP<=SP-1;state<=CALL_a;					   
				when CALL_a => ramAddr <= std_logic_vector(SP);state<=CALL_b;		
				when CALL_b =>	ramDin<= std_logic_vector(x"00"&PC);ramWE<='1';state<=CALL_c;
				when CALL_c =>	ramWE<='0';PC<=IR(7 downto 0);state<=fetch;			

            --PUSHI					
            when PUSHI   => 	SP<=SP-1; state<=PUSHI_a;			
				when PUSHI_a => ramAddr <= std_logic_vector(AC(7 downto 0));state<=PUSHI_b;			     
				when PUSHI_b => state<=PUSHI_c;
				when PUSHI_c => AUX <= unsigned(ramDout);state<=PUSHI_d;	
				when PUSHI_d => ramAddr <= std_logic_vector(SP);state<=PUSHI_e;		
				when PUSHI_e => ramDin<= std_logic_vector(AUX);ramWE<='1';state<=PUSHI_f;
				when PUSHI_f => ramWE<='0';state<=fetch;				
					
            --POPI					
 				when POPI   => ramAddr <= std_logic_vector(SP);state<=POPI_a;			     
				when POPI_a => state<=POPI_b;
				when POPI_b => AUX <= unsigned(ramDout);state<=POPI_c;	
				when POPI_c => ramAddr <= std_logic_vector(AC(7 downto 0));state<=POPI_d;		
				when POPI_d => ramDin<= std_logic_vector(AUX);ramWE<='1';state<=POPI_e;
				when POPI_e => ramWE<='0';SP<=SP+1;state<=fetch;								
 
				--PUSH					
            when PUSH   => SP<=SP-1;state<=PUSH_a;							   
				when PUSH_a => ramAddr <= std_logic_vector(SP);state<=PUSH_b;		
				when PUSH_b =>	ramDin<= std_logic_vector(AC);ramWE<='1';state<=PUSH_c;
				when PUSH_c =>	ramWE<='0';state<=fetch;

				--POP
				when POP   => ramAddr <= std_logic_vector(SP);state<=POP_a;			     
				when POP_a => state<=POP_b;
				when POP_b => AC <= signed(ramDout);SP<=SP+1;state<=fetch;	            					

           --SWAP					
           when SWAP   => TMP <= unsigned(AC(7 downto 0)); AC <= signed(x"00"&SP);state<=SWAP_a;
			  when SWAP_a => SP <= TMP;state<=fetch;
			      								
           --INSP
			  when INSP => SP <= SP+IR(7 downto 0);state<=fetch;
										
			  --DESP
			  when DESP => SP <= SP-IR(7 downto 0);state<=fetch;
															
           --INPAC
			  when INPAC =>
				   inFlags<=std_logic_vector(aux_inFlags);
				   if enter = '1' then 
					  AC<=signed(Din);
					  inFlags<=(others=>'0');
					  aux_inFlags<=SHIFT_LEFT (aux_inFlags,1);
					  state<=fetch;
					end if;										
					
           --OUTAC
			  when OUTAC =>
               outFlags<=std_logic_vector(aux_outFlags);				
					Dout <= std_logic_vector(AC);
					if enter = '1' then 
					   outFlags<=(others=>'0');
						Dout <=(others => '0');
						aux_outFlags<=SHIFT_LEFT (aux_outFlags,1);					
						state<=fetch;
					end if;					
					
           --HALT					
			  when HALT => done<='1';
			  
			  --OTHERS
			  when others => NULL;
			  
			end case;										
		end if;
	end process;
end Behavioral;



