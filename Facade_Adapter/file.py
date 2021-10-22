from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from starlette.responses import JSONResponse
from starlette.requests import Request
from bs4 import BeautifulSoup
import uvicorn
import requests

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")
app = FastAPI(title="main xml", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GetPage:
    url = ''
    page = ''

    def __init__(self, url: str):
        self.url = url

    def get_page(self):
        page = requests.get("https://russian-trade.com/coronavirus-russia/")
        page = page.content.decode()
        self.page = page
        return page


# адаптер
class ParsePage:
    data = ''
    result = ''

    def __init__(self, data: str):
        self.data = data

    def parse(self):
        soup = BeautifulSoup(self.data, 'lxml')
        table = soup.find("table", id="curs_special")
        self.result = []
        for tr in table.find_all("tr"):
            td = tr.find_all("td")
            if td:
                self.result.append({"region": td[1].text, "count": td[2].text.split("<br/>")[0]})
        return self.result


# фасад
class Facade:

    def __init__(self):
        pass

    def show_stat(self):
        p = GetPage("https://russian-trade.com/coronavirus-russia/")
        page = p.get_page()

        d = ParsePage(page)
        data = d.parse()


'''@app.get("/stat")
def get_stat():
    p = GetPage("https://russian-trade.com/coronavirus-russia/")
    page = p.get_page()

    d = ParsePage(page)
    data = d.parse()
    print(data)

    return data


templates = Jinja2Templates(directory="templates")
@app.get("/page")
async def page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})'''

'''page = requests.get("https://russian-trade.com/coronavirus-russia/")
    page = page.content.decode()
    soup = BeautifulSoup(page, 'lxml')
    table = soup.find("table", id="curs_special")

    data = []
    for tr in table.find_all("tr"):
        td = tr.find_all("td")
        if td:
            data.append({"region": td[1].text, "count": td[2].text.split("<br/>")[0]})'''