from dotenv import load_dotenv
import uvicorn

load_dotenv()

if __name__ == "__main__":
    from service import app

    uvicorn.run(app, host="0.0.0.0", port=8080)