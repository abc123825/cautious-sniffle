import asyncio

import httpx


async def screenshot_to_pdf_and_png(url, path, width=1024, height=9680, png=1800):
    url = f"https://mini.s-shot.ru/{width}x{height}/PNG/{png}/?{url}"
    async with httpx.AsyncClient(timeout=200) as client:
        r = await client.get(url)
        with open(path, "wb") as f:
            f.write(r.content)
        return path


async def webScreenShot(url, path):
    await screenshot_to_pdf_and_png(url, path, 1080, 980, 2024)


if __name__ == '__main__':
    asyncio.run(webScreenShot("https://prts.wiki/w/波登可", "./test.png"))
    #asyncio.run(screenshot_to_pdf_and_png("https://prts.wiki/w/斯卡蒂", "./test.png"))

    #webScreenShoot("https://prts.wiki/w/w","test.png",1200,7500)
