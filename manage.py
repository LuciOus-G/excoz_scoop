import sys
import uvicorn

try:
    import core
except ImportError as exc:
    raise ImportError("Couldn't import FastApi Instance.")


def execute(options):
    host = "localhost"
    port = 5000
    uvicorn.run("core:app", host=host, port=port, reload=True)


action_map = {
    "runserver": execute,
}

if __name__ == "__main__":
    args = sys.argv[1:]
    action = args[0]
    options = args[1:]
    try:
        action_map[action](options)
    except Exception as exc:
        raise exc
