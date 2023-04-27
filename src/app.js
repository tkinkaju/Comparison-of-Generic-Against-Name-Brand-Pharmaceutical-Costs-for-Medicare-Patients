// Copyright (c) 2023 Uber Technologies, Inc.
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

import React, {Component, useState} from 'react';
import AutoSizer from 'react-virtualized/dist/commonjs/AutoSizer';
import styled, {ThemeProvider} from 'styled-components';
import window from 'global/window';
import {connect} from 'react-redux';

import {theme} from '@kepler.gl/styles';
import Banner from './components/banner';
import Announcement, {FormLink} from './components/announcement';
import {replaceLoadDataModal} from './factories/load-data-modal';
import {replaceMapControl} from './factories/map-control';
import {replacePanelHeader} from './factories/panel-header';
import {AUTH_TOKENS, DEFAULT_FEATURE_FLAGS} from './constants/default-settings';
import {messages} from './constants/localization';
import sertralineData from './../map source data/2020/statesSummaries/Sertraline Hcl'
// import { config } from './Pages/KeplerConfig';
import config from './Pages/KeplerConfig2'
import SelectYear from './components/customSelectYear';
import SelectScale from './components/customSelectScale'
import SelectDrug from './components/customSelectDrug'
import ButtonSearch from './components/customButton'
import {processCsvData, processGeojson} from '@kepler.gl/processors';
import routedData from './Pages/DataRouting'
import mapBoxToken from './Pages/MapBoxToken'

import {
  loadRemoteMap,
  loadSampleConfigurations,
  onExportFileSuccess,
  onLoadCloudMapSuccess
} from './actions';

import {loadCloudMap, addDataToMap, addNotification, replaceDataInMap, wrapTo} from '@kepler.gl/actions';
import {CLOUD_PROVIDERS} from './cloud-providers';

const KeplerGl = require('@kepler.gl/components').injectComponents([
  replaceLoadDataModal(),
  replaceMapControl(),
  replacePanelHeader()
]);

var year = 2020;
var scale = "statesSummaries";
var drug = "Sertraline Hcl";
var globalProps = null;
export function updateYear(newYear){
  year = newYear
}
export function updateScale(newScale){
  scale = newScale
}
export function updateDrug(newDrug){
  drug = newDrug
}

function updateMapAtStart(props){
  const processedData = processCsvData(sertralineData)
  const dataset = { info: { label: "Ratio of Name Brand", id: "population_data" }, data: processedData };
  props.dispatch(wrapTo("map", addDataToMap({datasets:dataset, config})))
} 

export async function updateMap(props){
  const processedData = await routedData(year, drug, scale)
  const dataset = { info: { label: "Ratio of Name Brand", id: "population_data" }, data: processedData };
  props.dispatch(wrapTo("map", addDataToMap({datasets:dataset, config})))
}

const keplerGlGetState = state => state.demo.keplerGl;

const GlobalStyle = styled.div`
  font-family: ff-clan-web-pro, 'Helvetica Neue', Helvetica, sans-serif;
  font-weight: 400;
  font-size: 0.875em;
  line-height: 1.71429;

  *,
  *:before,
  *:after {
    -webkit-box-sizing: border-box;
    -moz-box-sizing: border-box;
    box-sizing: border-box;
  }

  ul {
    margin: 0;
    padding: 0;
  }

  li {
    margin: 0;
  }

  a {
    text-decoration: none;
    color: ${props => props.theme.labelColor};
  }
`;


class App extends Component {
  state = {
    showBanner: false,
    width: window.innerWidth,
    height: window.innerHeight
  };

  componentDidMount(){
    updateMapAtStart(this.props)
  }

 

  render() {
    return (
      <ThemeProvider theme={theme}>
        <GlobalStyle
          // this is to apply the same modal style as kepler.gl core
          // because styled-components doesn't always return a node
          // https://github.com/styled-components/styled-components/issues/617
          ref={node => {
            node ? (this.root = node) : null;
          }}
        >
          <div
            style={{
              transition: 'margin 1s, height 1s',
              position: 'absolute',
              width: '100%',
              height: '100%',
              left: 0,
              top: 0
            }}
          >
            <AutoSizer>
              {({height, width}) => (
                <KeplerGl
                  mapboxApiAccessToken={mapBoxToken}
                  id="map"
                  /*
                   * Specify path to keplerGl state, because it is not mount at the root
                   */
                  getState={keplerGlGetState}
                  width={width}
                  height={height}
                  cloudProviders={CLOUD_PROVIDERS}
                  localeMessages={messages}
                  onExportToCloudSuccess={onExportFileSuccess}
                  onLoadCloudMapSuccess={onLoadCloudMapSuccess}
                  featureFlags={DEFAULT_FEATURE_FLAGS}
                />
              )}
            </AutoSizer>
            <div style={{ backgroundColor: 'white', width: 130, height:260, position: 'absolute', zIndex: 100, bottom: 10, right: 10}}><SelectYear/><SelectScale/><SelectDrug/><ButtonSearch props={this.props}/></div>
            <div style={{ backgroundColor: 'white', width: 500, height:60, position: 'absolute', zIndex: 100, top: 20, right: 60, alignItems:"center"}}><p>  Year: {year}   Scale: {scale}   Drug: {drug}</p></div>
          </div>
          
        </GlobalStyle>
      </ThemeProvider>
    );
  }
}

const mapStateToProps = state => state;
const dispatchToProps = dispatch => ({dispatch});

export default connect(mapStateToProps, dispatchToProps)(App);
