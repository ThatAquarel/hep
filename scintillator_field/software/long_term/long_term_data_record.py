import time
import logging

from scintillator_display.display.impl_a.data_manager import test as DataRecorder


def record():
    logger = logging.getLogger("RECORDER")
    data_recorder = DataRecorder(debug=False)
    
    while True:
        if not data_recorder.has_data():
            time.sleep(0.001)
            continue
        
        value = data_recorder.get_data_from_arduino():
        logger.info(value)

        lsb = value & 0xFFFFFF
        b1 = (lsb >> 16) & 0xFF
        b2 = (lsb >> 8) & 0xFF
        b3 = lsb & 0xFF

        logger.debug("receive trigger: SiPM status")
        logger.debug(f"    {b1:02x}          {b2:02x}          {b3:02x}")
        logger.debug(f"    {b1:08b}    {b2:08b}    {b3:08b}")


def main():
    logger = logging.getLogger("MAIN")

    while True:
        try:
            logger.info("start recorder")
            record()
        except Exception as e:
            logger.warning(f"restart recorder because {e}")
            ...


if __name__ == "__main__":
    logging.basicConfig(
        filename=f"start_{time.time()}.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )

    main()
