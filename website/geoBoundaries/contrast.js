import 'assets/css/ol/ol.css';
import Map from 'assets/js/ol/Map';
import OSM from 'assets/js/ol/source/OSM';
import TileLayer from 'assets/js/ol/layer/Tile';
import View from 'assets/js/ol/View';
import {FullScreen, defaults as defaultControls} from 'assets/js/ol/control';

var view = new View({
  center: [-9101767, 2822912],
  zoom: 14,
});

var map = new Map({
  controls: defaultControls().extend([
    new FullScreen({
      source: 'fullscreen',
    }) ]),
  layers: [
    new TileLayer({
      source: new OSM(),
    }) ],
  target: 'map',
  view: view,
});
