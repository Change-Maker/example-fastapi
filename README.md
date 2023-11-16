# FastAPI App Example

**Environment:**

- Python v3.10.7
- Node v20.9.0

## 1. Requirements

- Python 3.10+

    This example uses `|` operator on type annotations (PEP 604).

- Python 3.8+

    This example uses `:=` (Walrus) operator on file chunked reading (PEP 572).

## 2. Setup Environment

1. Create Python virtual environment.

    ```bash
    python -m venv py310venv
    ```

2. Activate the Python virtual environment.

    ```bash
    source py310venv/bin/activate
    ```

3. Upgrade `pip` and install dependencies.

    ```bash
    python -m pip install --no-cache-dir --upgrade pip
    python -m pip install --no-cache-dir --upgrade -r requirements.txt
    ```

## 3. Usage

Get into `src/client/` folder and install dependencies:

```bash
npm install
```

Build React app by running the following commands in `src/client/` folder:

```bash
npm run build
```

Afterwards, run `python main.py` in `src/fastapi_app/` folder to start service.

### 3.1 Development mode

First, add `proxy` option into `src/client/package.json` file:

```jsonc
{
  // ...
  "proxy": "http://localhost:3001"
}
```

And start React app by running the following command in `src/client/` folder:

```bash
npm start
```

(If you encount any problem with command above, check [docs/react.md](./docs/react.md)
for more information.)

This will proxy the request from the React app to FastAPI backend.

Then get into `src/fastapi_app/` folder and start FastAPI backend in development
mode:

```bash
MODE="dev" python main.py
```

In this mode, it will reload automatically if you save the changes to files
either in `src/fastapi_app/` folder or `src/client/` folder.

Now, open browser and get to `http://localhost:3000`.

Run the following code in the browser console:

```js
fetch("/hello").then((res) => res.json()).then((data) => console.log(data));
```

It should receive `world` from the backend.

### 3.2 File logger

To enable file logger, change `logger.enable` to `true` in
`src/fastapi_app/configs/settings.json` file.

The log files will be put in `src/fastapi_app/logs/` folder.
To change the location to place log files, change `logger.path` in
`src/fastapi_app/configs/settings.json` file.

### 3.3 Default console logger

To change the log level of default console logger, set `LOGURU_LEVEL`
environment variable, e.g. set it to `INFO`:

```bash
LOGURU_LEVEL="INFO" python main.py

# or if using Docker containers:
docker run -e LOGURU_LEVEL="INFO" -p 3001:3001 -d example-fastapi
```

To disable the default console logger, change the following lines in
`src/fastapi_app/main.py` file:

```py
if settings.logger is not None:
    logger_util.setup_logger(settings.logger, True)
```

### 3.4 Docker

You should build React app before building Docker images.

The examples below use `example-fastapi` as the image name.

#### 3.4.1 Building images

To build a Docker image:

```bash
docker build -t example-fastapi .
```

Run a container (the default port is `3001`):

```bash
docker run -p 3001:3001 -d example-fastapi
```

#### 3.4.2 Environment Only

To build a Docker image that only contains environment:

```bash
docker build -t example-fastapi:env-only -f Dockerfile.env_only .
```

Run a container:

```bash
docker run -p 3001:3001 -v ./src:/ws/src -d example-fastapi:env-only
```

## Troubleshooting

- **isort sorts imports in wrong order.**

    Refer to [Wrong order in import when using sort imports in vscode #14254](https://github.com/microsoft/vscode-python/issues/14254)

    **Solution:** Add `.vscode/settings.json` to your workspace:

    ```json
    {
      "isort.args": [
        "--src=${workspaceFolder}/src/fastapi_app"
      ]
    }
    ```

- **Browser doesn't reflect changes made in the files in `client` folder.**

  Browser might cache the content before changes made.

  To disable browser caching, open the developer tools (press the `F12` key
  generally) and get into **Network** tab then check **Disable cache** checkbox.

  Now refresh the website, it should reflect changes.
