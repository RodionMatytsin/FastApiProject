import uvicorn
import main


if __name__ == '__main__':
    uvicorn.run(main.app, port=6868, host='localhost', use_colors=True)
