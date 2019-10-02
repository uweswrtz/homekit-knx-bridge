import asyncio
from xknx import XKNX

async def telegram_received_cb(telegram):
    print("Telegram received: {0}".format(telegram))

async def main():
    xknx = XKNX(config="xknx.yaml',telegram_received_cb=telegram_received_cb)
    await xknx.start(daemon_mode=True)
    await xknx.stop()

if __name__ == "__main__":
  # pylint: disable=invalid-name
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.close()