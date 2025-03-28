yosys -p 'synth_ice40 -top top -json latching_register.json' latching_register.v
nextpnr-ice40 --package tq144 --json latching_register.json --pcf latching_register.pcf --asc latching_register.asc
icepack latching_register.asc latching_register.bin

dd if=/dev/zero ibs=1 count=2097152 > padding.bin
dd if=latching_register.bin of=padding.bin conv=notrunc
flashrom -p serprog:dev=/dev/ttyACM0:4000000 -w padding.bin -c W25Q16.V

flashrom -p serprog:dev=/dev/ttyACM0:4000000 -r file-to-save.bin -c W25Q16.V
flashrom -p serprog:dev=/dev/ttyACM0:4000000 -E -c W25Q16.V
