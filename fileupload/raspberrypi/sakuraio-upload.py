import logging
import time
from sakuraio.hardware.rpi import SakuraIOSMBus

logger = logging.getLogger(__name__)

def upload(filename):

    logger.info("start upload %s", filename)

    data = None
    with open(filename, "rb") as f:
        data = f.read()

    sakuraio = SakuraIOSMBus()

    # Check online
    if not sakuraio.get_is_online():
        logger.error("Offline")
        return

    # Start upload
    logger.info("Start upload size=%d", len(data))
    sendChannels(sakuraio, [(1, len(data))])

    sequence = 0
    while len(data) > 0:
        # Send chunk

        channels = [(2, sequence)]
        chunk = data[:8*15]

        logger.info("Send chunk sequence=%d size=%d", sequence, len(chunk))

        while len(chunk):
            d = chunk[:8] + b"\x00\x00\x00\x00\x00\x00\x00\x00"
            channels.append((2, d[:8]))
            chunk = chunk[8:]

        try:
            sendChannels(sakuraio, channels)
        except KeyboardInterrupt:
            raise
        except:
            logger.exception("Send chunk error")
            continue

        sequence += 1
        data = data[8*15:]

    # Finish upload
    logger.info("Finish upload")
    sendChannels(sakuraio, [(3, 0)])


def sendChannels(sakuraio, channels):
    sakuraio.clear_tx()
    for channel in channels:
        sakuraio.enqueue_tx(channel[0], channel[1])

    sakuraio.send()

    while True:
        queue = sakuraio.get_tx_status()["queue"]
        if queue == 0x00:
            # success
            return
        if queue == 0x01:
            # sending
            time.sleep(0.01)
            continue
        if queue == 0x02:
            # error
            raise Exception()


if __name__ == "__main__":
    import sys
    filename = sys.argv[1]

    formatter = logging.Formatter("[%(asctime)s] [%(process)d] [%(name)s] [%(levelname)s] %(message)s")
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    try:
        upload(filename)
    except:
        logger.exception("error")
