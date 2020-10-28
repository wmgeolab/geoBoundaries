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

sudo apt-get update
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.36.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
nvm install 14.15.0
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
apt-get install git
git clone https://github.com/wmgeolab/gbRelease.git
cd gbRelease

#=========================
For Dev:
git clone https://github.com/DanRunfola/gbRelease.git
git fetch --all
git checkout gD
#=========================

cd website
cd geoDesc
npm install




#NODE_OPTIONS="--max-old-space-size=8192"
#export NODE_OPTIONS

