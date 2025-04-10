# Variables
VERILOG_FILES := $(wildcard *.v)        # Find all .v files in the current directory

build: $(VERILOG_FILES)
	@yosys -p 'synth_ice40 -top top -json latching_register.json' $(VERILOG_FILES)
	@nextpnr-ice40 --package tq144 --json latching_register.json --pcf latching_register.pcf --asc latching_register.asc
	@icepack latching_register.asc latching_register.bin


synth: $(VERILOG_FILES)
	@yosys -p 'synth_ice40 -top top -json latching_register.json' $(VERILOG_FILES)

route:
	@nextpnr-ice40 --package tq144 --json latching_register.json --pcf latching_register.pcf --asc latching_register.asc --placer-heap-cell-placement-timeout 10

flash:
	@dd if=/dev/zero ibs=1 count=2097152 > padding.bin
	@dd if=latching_register.bin of=padding.bin conv=notrunc
	@flashrom -p serprog:dev=/dev/ttyACM0:4000000 -w padding.bin -c W25Q16.V

verify:
	@flashrom -p serprog:dev=/dev/ttyACM0:4000000 -v padding.bin -c W25Q16.V

clean:
	@rm latching_register.asc latching_register.bin latching_register.json padding.bin
