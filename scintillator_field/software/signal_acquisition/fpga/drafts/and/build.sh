yosys -p 'synth_ice40 -top top -json and.json' and.v
nextpnr-ice40 --package tq144 --hx1k --json and.json --pcf and.pcf --asc and.asc
icepack and.asc and.bin

dd if=/dev/zero ibs=1 count=2097152 > padding.bin
dd if=and.bin of=padding.bin conv=notrunc
flashrom -p serprog:dev=/dev/ttyACM0:4000000 -w padding.bin -c W25Q16.V

flashrom -p serprog:dev=/dev/ttyACM0:4000000 -r file-to-save.bin -c W25Q16.V
flashrom -p serprog:dev=/dev/ttyACM0:4000000 -E -c W25Q16.V
