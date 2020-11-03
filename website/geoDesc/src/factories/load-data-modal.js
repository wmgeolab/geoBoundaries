// Copyright (c) 2020 Uber Technologies, Inc.
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
// THE SOFTWARE.

import {LoadDataModalFactory, withState} from 'kepler.gl/components';
import {LOADING_METHODS} from '../constants/default-settings';

import geoBoundariesAtlas from '../components/load-data-modal/load-gb-atlas';
import SampleMapGallery from '../components/load-data-modal/sample-data-viewer';
import LoadRemoteMap from '../components/load-data-modal/load-remote-map';
import LoadCuratedMap from '../components/load-data-modal/load-curated';
import SampleMapsTab from '../components/load-data-modal/sample-maps-tab';
import {loadRemoteMap, loadCuratedMap, loadSample, loadSampleConfigurations} from '../actions';

const CustomLoadDataModalFactory = (...deps) => {
  const LoadDataModal = LoadDataModalFactory(...deps);
  const defaultLoadingMethods = LoadDataModal.defaultProps.loadingMethods;
  const additionalMethods = {
    remote: {
      id: LOADING_METHODS.remote,
      label: 'Load from Web',
      elementType: LoadRemoteMap
    },
    sample: {
      id: LOADING_METHODS.sample,
      label: 'Example Projects',
      elementType: SampleMapGallery,
      //tabElementType: SampleMapsTab
    },
    atlas: {
      id: LOADING_METHODS.atlas,
      label: 'geoBoundaries Atlas',
      elementType: geoBoundariesAtlas,
      tabElementType: SampleMapsTab
    },
    curated: {
      id: LOADING_METHODS.curated,
      label: 'Analysis-Ready Datasets',
      elementType: LoadCuratedMap
    }
  };

  // add more loading methods
  LoadDataModal.defaultProps = {
    ...LoadDataModal.defaultProps,
    loadingMethods: [
      additionalMethods.sample,
      additionalMethods.curated,
      defaultLoadingMethods.find(lm => lm.id === 'upload'),
      additionalMethods.atlas
      //additionalMethods.remote
      //defaultLoadingMethods.find(lm => lm.id === 'storage'),
    ]
  };

  return withState([], state => ({...state.demo.app, ...state.demo.keplerGl.map.uiState}), {
    onLoadSample: loadSample,
    onLoadRemoteMap: loadRemoteMap,
    onLoadCuratedMap: loadCuratedMap,
    loadSampleConfigurations
  })(LoadDataModal);
};

CustomLoadDataModalFactory.deps = LoadDataModalFactory.deps;

export function replaceLoadDataModal() {
  return [LoadDataModalFactory, CustomLoadDataModalFactory];
}
