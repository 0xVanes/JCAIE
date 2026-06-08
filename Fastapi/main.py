# ada di 127.0.0.1:8000
## tambah 127.0.0.1:8000/docs buat liat lebih jelas semua endpoints
### 127.0.0.1:8000/redoc
#### FASTApi buat yang ringan, Django buat yg berat
##### nonton pixegami
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Make a todo-list item (This is a modeled obj so normal curl -X POST or GET won't work)
## It needs to be called in JSON payload
### Has 2 things: text and is_done
class Item(BaseModel):
    text: str = None
    is_done: bool = False


## Bikin to do items (harus ada liat dan bikin)
items = []

# Define path with .get
@app.get("/")
def root(): # lebih aman pake async def root():
    return {"Hello": "world"}
# run uvicorn main: app --reload
## main: app -> main = nama filenya app FastAPI() variable

@app.post("/items") # Add routes kyk items (127.0.0/8000/items)
# def create_item(item: str): #item is a query parameter
#     items.append(item)
#     return items # return all the list (items) or the appended (item)
# CHECK! curl -X POST -H "Content-Type: application/json" "http://127.0.0.1:8000/items?item=apple"
## Error ga nambah di items arraynya. kalau item=orange ya orange aja. applenya ilang

def create_item(item: Item):
    items.append(item)
    return items
# curl -X POST -H "Content-Type: application/json" -d "{\"text\": \"apple\"}" "http://127.0.0.1:8000/items"

# Lihat items sepcifically item_id
## Every reload resets items to an empty array
@app.get("/items/{item_id}", response_model=Item) #jadinya /items/1 or /items/2 #response_model Item aja atau list[Item]
# def get_item(item_id: int) -> str:
    # item = items[item_id]
    # return item
# curl -X GET http://127.0.0.1:8000/items/0
# add error handling
def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code = 404, detail =f"Item {item_id} not found")
    
@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10): #default = 10, insert limit number
    return items[0:limit]
# curl -X GET "http://127.0.0.1:8000/items?limit=3"