import logging
import os

from config import autoclean


async def auto_clean(popped):
    """
    Remove files from autoclean list, if they are not present in the list anymore.
    :param popped:
    :return:
    """
    try:
        rem = popped["file"]
        autoclean_copy = autoclean.copy()
        for item in autoclean_copy:
            if item == rem:
                autoclean.remove(item)

        count = autoclean.count(rem)
        if count == 0:
            if not ("vid_" in rem or "live_" in rem or "index_" in rem):
                try:
                    if os.path.exists(rem):
                        os.remove(rem)
                except Exception as e:
                    logging.error(f"Error in auto_clean: {e}")
    except Exception as e:
        logging.error(f"Error in auto_clean: {e}")
