Notes for getting this setup on a new server:

sudo apt-get update
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.36.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
nvm install 14.15.0
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
apt-get install git
git clone https://github.com/wmgeolab/geoBoundaries.git
cd geoBoundaries

#=========================
For Dev:
git clone https://github.com/DanRunfola/geoBoundaries.git
git fetch --all
git checkout gD
#=========================

cd website
cd geoDesc
npm install
export MapboxAccessToken=<your_mapbox_token>
npm start



