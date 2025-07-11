from fastapi import FastAPI, Request, Depends
import db_conn
from torrent import Torrent
import traceback
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add this after creating your FastAPI app object
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend URL, e.g. ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "rarbg_db.sqlite"

async def get_db():
    """Return a database connection for use as a dependency.
    This connection has the Row row factory automatically attached."""
    db = db_conn.RarbgDatabase()
    await db.connect(DB_FILE)

    try:
        yield db
    finally:
        await db.close()

@app.get("/pubapi_v2.php")
async def req(request: Request, db: db_conn.RarbgDatabase = Depends(get_db)):
    try:
        request_dict = dict(request.query_params.items())

        if "get_token" in request_dict:
            return {"token": "1234567890"}

        if "mode" in request_dict:
            if request_dict["mode"] == "search":
                return await search(db, request_dict)
            elif request_dict["mode"] == "list":
                return await list_cat(db, request_dict)
        return {"detail": "Invalid mode"}
    except Exception as e:
        traceback.print_exc()  # Print the stack trace on server console
        return JSONResponse(status_code=500, content={"detail": str(e)})

def get_categories(request_dict: dict):
    cats = request_dict.get("category", None)
    if cats is not None:
        cats = cats.split(";")
        cats = [int(cat) for cat in cats]
    return cats

async def search(db: db_conn.RarbgDatabase, request_dict: dict):
    try:
        list_of_categories = get_categories(request_dict)
        limit = int(request_dict.get("limit", 100))  # <-- convert to int here
        imdb = request_dict.get("search_imdb", None)
        search_string = request_dict.get("search_string", None)
        res = await db.search(list_of_categories, limit, imdb, search_string)
        return build_response(res, True)

    except Exception as e:
        print("DB Search Error:", e)
        raise


async def list_cat(db: db_conn.RarbgDatabase, request_dict, limit: int = 100):
    categories = get_categories(request_dict)
    if categories is None:
        raise ValueError("No categories provided")
    
    res = await db.list_from_categories(categories, limit)
    return build_response(res, True)

def build_response(torrents: list[Torrent], extended: bool = False):
    res = {"torrent_results": []}
    if not extended:
        for t in torrents:
            res["torrent_results"].append({
                "filename": t.title,
                "category": "Not Available",
                "download": "magnet:?xt=urn:btih:" + t.hash_code,
            })
    else:
        for t in torrents:
            res["torrent_results"].append({
                "title": t.title,
                "category": "Not Available",
                "download": t.build_magnet_link(),
                "seeders":10,
                "leechers":10,
                "size":t.size,
                "pubdate": t.time +" +0000",
                "episode_info":{
                    "imdb":t.imdb,
                    "tvrage": None,
                    "tvdb":None,
                    "themoviedb":None
                },
                "ranked":1,
                "info_page":"https://torrentapi.org/"
            })
    return res
