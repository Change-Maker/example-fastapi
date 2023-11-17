# Next.js

**Environment:**

- Node v20.9.0
- create-next-app v14.0.3

## Integrating FastAPI with Next.js

Initialize Next.js app:

```text
src$ npx create-next-app --typescript client
✔ Would you like to use ESLint? … Yes
✔ Would you like to use Tailwind CSS? … Yes
✔ Would you like to use `src/` directory? … No
✔ Would you like to use App Router? (recommended) … Yes
✔ Would you like to customize the default import alias (@/*)? … No
Creating a new Next.js app in /home/user/Workspaces/template_ws/example-fastapi/src/client.
```

Modify `src/client/next.config.js` file to map any requests to `/:path*` to the
FastAPI API:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  rewrites: async () => {
    return [
      {
        source: '/:path*',
        destination: 'http://localhost:3001/:path*',
      },
      {
        source: '/docs',
        destination: 'http://localhost:3001/docs',
      },
      {
        source: '/openapi.json',
        destination: 'http://localhost:3001/openapi.json',
      },
    ];
  },
};

module.exports = nextConfig;
```

As code block above:

- Our FastAPI service is under `http://localhost:3001`.
- Our FastAPI API is under `/`.

### Development

Start FastAPI service in development mode:

```text
src/fastapi_app$ MODE="dev" python main.py
```

Start Next.js app in development mode:

```text
src/client$ npm run dev
> client@0.1.0 dev
> next dev

 ⚠ Port 3000 is in use, trying 3001 instead.
 ⚠ Port 3001 is in use, trying 3002 instead.
   ▲ Next.js 14.0.3
   - Local:        http://localhost:3002

 ✓ Ready in 2.5s
```

It will show you Next.js app is running on which port. As shown above, it runs
on `3002` port.

Afterwards, open browser and get into `http://localhost:3002`. The default
Next.js app web page is shown.

Now open **Developer Tools** (generally press `F12`) and enter this command in
console to send a request:

```js
fetch("/hello").then((res) => res.json()).then((data) => console.log(data));
```

It will response `world` to you.

### Production

This also use the way that proxy requests to the FastAPI service.

Build Next.js app:

```text
src/client$ npm run build
```

Start FastAPI service:

```text
src/fastapi_app$ python main.py
```

To change the port where the Next.js app runs, modify `scripts.start` option in
`src/client/package.json` file, for example, runs on `3002` port:

```jsonc
{
  // ...
  "scripts": {
    // ...
    "start": "next start -p 3002",
  // ...
  },
  // ...
}
```

Afterwards, start the Next.js app:

```text
src/client$ npm start
```

## Docker

To add support for Docker, copy the [Dockerfile](https://github.com/vercel/next.js/blob/canary/examples/with-docker/Dockerfile)
into `src/client/` folder and add `output: 'standalone'` to
`src/client/next.config.js` file:

```js
// next.config.js
module.exports = {
  // ... rest of the configuration.
  output: 'standalone',
}
```

Run the following command in `src/client/` folder to build Docker image:

```bash
docker build -t nextjs-app .
```

To make it easy to proxy requests to FastAPI service, we run the Next.js app
container with `host` network:

```bash
docker run --network host -it nextjs-app
```

### Change the port number

If you want to change the port that the Next.js app runs on, change the
container `PORT` environment variable, for example, `3005`:

```bash
docker run --network host --env PORT="3005" -it nextjs-app
```

### Access FastAPI service which runs in another container

1. Create a Docker network, for example, `my-nw`.

    ```bash
    docker network create -d bridge my-nw
    ```

2. Change the proxy hostname in `src/client/next.config.js` file.

    Since we will use `fastapi-app` as the container name of the FastAPI service,
    the hostname should be `fastapi-app`:

    ```js
    /** @type {import('next').NextConfig} */
    const nextConfig = {
      output: 'standalone',
      rewrites: async () => {
        return [
          {
            source: '/:path*',
            destination: 'http://fastapi-app:3001/:path*',
          },
          {
            source: '/docs',
            destination: 'http://fastapi-app:3001/docs',
          },
          {
            source: '/openapi.json',
            destination: 'http://fastapi-app:3001/openapi.json',
          },
        ];
      },
    };

    module.exports = nextConfig;
    ```

3. Build the Next.js app Docker image.

    We use `nextjs-app` as the image name:

    ```text
    src/client$ docker build -t nextjs-app .
    ```

4. Start the Next.js app.

    ```bash
    docker run -p 3000:3000 --network my-nw -it nextjs-app
    ```

    - `-p 3000:3000`: To enter Next.js app on host, we do a port mapping.
    - `--network my-nw`: To proxy requests to the FastAPI service which runs in
      another container, we use the network we created above.

5. Start the FastAPI service.

    ```bash
    docker run --name fastapi-app --network my-nw -it fastapi-app
    ```

## References

- [Next.js FastAPI Starter](https://github.com/digitros/nextjs-fastapi)
- [Integrate FastAPI Framework with Next.js and Deploy](https://github.com/wpcodevo/nextjs-fastapi-framework)
