module top (
    // system clock
    input wire sys_clk,           // 14.4 mhz
    output wire sys_clk_pll,
    output wire sys_clk_pll_lock, // high -> pll lock

    // data registers
    input wire [23:0] S,       // Set inputs (one per bit)
    output reg [23:0] Q,        // Non-inverting outputs

    // interface
    input wire rst_n,           // active-low reset (clears all latches)
    output reg trigger,
    output wire trigger_led,

    input wire spi_cs,          // chip select, active-low
    input wire spi_clk,          // spi clock
    output reg spi_miso,       // master in slave out

    // debug
    output reg counter_0,
    output reg counter_1
);

pll pll_inst (
    .clock_in(sys_clk),        // Input clock (14.4 MHz) STM32
    .clock_out(sys_clk_pll),
    .locked(sys_clk_pll_lock)
);

// Synchronizer registers for each bit (two-stage for each input)
reg [23:0] sync1, sync2; // sync1 and sync2 for each S[i]
integer i;

// shift-register output
// reg [23:0] shift_Q;
// reg [23:0] shift_reg = 24'd0;
// reg [4:0] bit_count = 5'd0;       // 5 bits needed for counting to 24

reg [23:0] shift_reg;
reg [4:0] bit_count;       // 5 bits needed for counting to 24

reg spi_clk_sync1, spi_clk_sync2;
reg spi_cs_sync1, spi_cs_sync2;

assign counter_0 = bit_count[0];
assign counter_1 = bit_count[1];

// difference detection
wire [23:0] diff;
assign diff = sync2 ^ Q;
assign trigger_led = trigger;

// input-latching
// always @(posedge sys_clk_pll or negedge rst_n or negedge spi_cs) begin
always @(posedge sys_clk_pll or negedge rst_n) begin
    if (!rst_n) begin
        Q <= 24'b0;          // Reset all latches when rst_n is LOW
        sync1 <= 24'b0;      // Clear first stage of synchronizers
        sync2 <= 24'b0;      // Clear second stage of synchronizers

        // clear shift register sync
        shift_reg <= 24'b0;
        bit_count <= 5'b0;
        spi_miso <= 1'b0;

        spi_clk_sync1 <= 1'b0; 
        spi_clk_sync2 <= 1'b0; 
        spi_cs_sync1 <= 1'b0; 
        spi_cs_sync2 <= 1'b0; 

        // clear trigger
        trigger <= 1'b0;

    end else begin
        // Synchronize the inputs with two stages
        sync1 <= S;         // First stage synchronizer
        sync2 <= sync1;     // Second stage synchronizer

        // Latch the output based on the synchronized input
        for (i = 0; i < 24; i = i + 1)
            if (sync2[i])
                Q[i] <= 1'b1;
        end

        // empty data filter trigger
        if (
            diff[1:0]   != 2'b00 &&
            diff[3:2]   != 2'b00 &&
            diff[5:4]   != 2'b00 &&
            diff[7:6]   != 2'b00 &&
            diff[9:8]   != 2'b00 &&
            diff[11:10] != 2'b00 &&
            diff[13:12] != 2'b00 &&
            diff[15:14] != 2'b00 &&
            diff[17:16] != 2'b00 &&
            diff[19:18] != 2'b00 &&
            diff[21:20] != 2'b00 &&
            diff[23:22] != 2'b00
        ) begin
            trigger <= 1'b1;
        end

        // previous spi signal
        // spi_clk_prev <= spi_clk;
        spi_clk_sync1 <= spi_clk;
        spi_clk_sync2 <= spi_clk_sync1;

        spi_cs_sync1 <=  spi_cs;
        spi_cs_sync2 <= spi_cs_sync1;

        // on CS low: begin SPI request
        // CPOL = 0
        // CPHA = 0
        if (!spi_cs_sync2) begin
        // if ((spi_cs_sync2 == 0) && (spi_cs_sync1 == 1)) begin
            // if no bit sent out: load register with latches
            if (bit_count == 0)
                shift_reg <= Q;

            // output on falling
            // if (spi_clk_prev == 1 && spi_clk == 0) begin
            if ((spi_clk_sync2 == 0) && (spi_clk_sync1 == 1)) begin
                spi_miso <= shift_reg[23]; // MSB
                shift_reg <= {shift_reg[22:0], 1'b0}; // shift left
                bit_count <= bit_count + 1;
            end

            // reset register when overflow
            if (bit_count == 24)
                bit_count <= 0;
        end else begin
            // on CS high: reset data
            bit_count <= 0;
            spi_miso <= 0;
        end

        // if ((spi_cs_sync2 == 1) && (spi_cs_sync1 == 0)) begin
        //     bit_count <= 0;
        //     spi_miso <= 0;
        // end
    end
end

endmodule