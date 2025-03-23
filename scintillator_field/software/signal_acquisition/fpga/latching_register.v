module top (
    input wire clk,           // Clock input for synchronization
    output wire clk_copy,
    output wire locked,
    input wire [7:0] S,       // Set inputs (one per bit)
    input wire rst_n,         // Global active-low reset (clears all latches)
    output reg [7:0] Q        // Non-inverting outputs
);

pll pll_inst (
    .clock_in(clk),        // Input clock (10 MHz)
    .clock_out(clk_copy),
    .locked(locked)            // Output clock (100 MHz)
);

// assign clk_copy = clk;

// Synchronizer registers for each bit (two-stage for each input)
reg [7:0] sync1, sync2; // sync1 and sync2 for each S[i]
integer i;

always @(posedge clk_copy or negedge rst_n) begin
    if (!rst_n) begin
        Q <= 8'b0;          // Reset all latches when rst_n is LOW
        sync1 <= 8'b0;      // Clear first stage of synchronizers
        sync2 <= 8'b0;      // Clear second stage of synchronizers
    end else begin
        // Synchronize the inputs with two stages
        sync1 <= S;         // First stage synchronizer
        sync2 <= sync1;     // Second stage synchronizer

        // Latch the output based on the synchronized input
        for (i = 0; i < 8; i = i + 1) begin
            if (sync2[i])   // Set output high if synchronized S[i] is asserted
                Q[i] <= 1'b1;
            // If sync2[i] is low, hold the previous state (Q[i] stays the same)
        end
    end
end

endmodule