# React

## Mount to a Non-root Path

For example, mount the React app under `/react-client` path in `src/main.py`:

```python
app.mount(
    "/react-client",
    StaticFiles(directory=REACT_BUILD_DIR, html=True),
    name="react_client",
)
```

We need to add `homepage` option into `src/react_client/package.json` file:

```jsonc
{
  // ...
  "homepage": "/react-client"
}
```

To build React app, run the following command in `src/react_client/` folder:

```bash
npm run build
```

Then run the following command in `src/fastapi_app/` folder:

```bash
python main.py
```

Now, the React app web page should be under
`http://localhost:3001/react-client/` URL.

## Troubleshooting

- **Proxy to backend raised
  `options.allowedHosts[0] should be a non-empty string`**

  Refer to [create-react-app GitHub Issue #12304](https://github.com/facebook/create-react-app/issues/12304)

  **Re-produce:**
  1. Add `proxy` to `src/client/package.json`:

      ```jsonc
      {
        // ...
        "proxy": "http://localhost:3001"
      }
      ```

  2. Run the following command in `src/client/` folder to start react app:

      ```bash
      npm start
      ```

  3. The error raised:

      ```text
      Invalid options object. Dev Server has been initialized using an options object that does not match the API schema.
        - options.allowedHosts[0] should be a non-empty string.
      ```

  **Workaround:** Start react app with `DANGEROUSLY_DISABLE_HOST_CHECK`
  environment variable to be set to `true`:

  ```bash
  DANGEROUSLY_DISABLE_HOST_CHECK=true npm start
  ```
