module top (
    input [7:0] D,   // 8-bit parallel data input
    input RST,        // Reset (clears all registers)
    input CLK,        // Clock signal for serial shifting
    input LOAD,       // Load signal (loads D into shift register)
    output reg Q      // Serial output
);
  
  reg [7:0] shift_reg;  // 8-bit shift register

  always @(posedge CLK or posedge RST) begin
    if (RST)
      shift_reg <= 8'b0;  // Reset: Fill shift register with zeros
    else if (LOAD)
      shift_reg <= ~D;      // Load **inverted** parallel data
    else
      shift_reg <= {shift_reg[6:0], 1'b0}; // Shift left, filling with 0s
  end

  assign Q = shift_reg[7];  // Output MSB (most significant bit)

endmodule
