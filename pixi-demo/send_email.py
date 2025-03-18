# python3 -m aiosmtpd --nosetuid --debug --debug --listen 0.0.0.0:8025 &

import asyncio
from email.message import EmailMessage

import aiosmtplib

from pathlib import Path


fname = Path("log.txt")

if fname.exists():
    with open("log.txt") as f:
        log = f.read()

    message = EmailMessage()
    message["From"] = "ocefpaf+pixi@gmail.com"
    message["To"] = "ocefpaf@gmail.com"
    message["Subject"] = "glideroftheday"
    message.set_content(f"{log}")

    asyncio.run(aiosmtplib.send(message, hostname="0.0.0.0", port=8025))
