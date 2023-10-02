from homework07.vkapi import config  # type: ignore
from homework07.vkapi.session import Session  # type: ignore

session = Session(config.VK_CONFIG["domain"])
