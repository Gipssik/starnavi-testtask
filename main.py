import uvicorn

if __name__ == "__main__":
    uvicorn.run("social_network.app:get_app", host="0.0.0.0", log_level="info")
