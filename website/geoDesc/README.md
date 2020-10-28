# Demo App

This is the src code  of kepler.gl demo app. You can copy this folder out and run it locally.

#### 1. Install

```sh
npm install
```

or

```sh
yarn
```


#### 2. Mapbox Token
add mapbox access token to node env

```sh
export MapboxAccessToken=<your_mapbox_token>
```

#### 3. Start the app

```sh
npm start
```

Notes
-> apt install nodejs
-> apt install build-essentials
-> npm install --save-dev @babel/preset-react
-> npm install --save-dev @babel/preset-env

echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
NODE_OPTIONS="--max-old-space-size=4096"
export NODE_OPTIONS
