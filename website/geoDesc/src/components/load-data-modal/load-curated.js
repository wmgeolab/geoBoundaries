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

// TODO: this will move onto kepler.gl core
import React, {Component} from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import {CORS_LINK} from '../../constants/default-settings';
import {FormattedHTMLMessage, FormattedMessage} from 'react-intl';
import {Button} from 'kepler.gl/components';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import DataTable from 'react-data-table-component';
import {regionOptions} from '../../../dynamicAssets/regionOptions'
import {data} from '../../../dynamicAssets/regionData'





const propTypes = {
  onLoadCuratedMap: PropTypes.func.isRequired
};


const columns = [
  {
    name: 'Variable',
    selector: 'title',
    sortable: true,
    grow:2,
    maxWidth:30,
    wrap:true
  },
  {
    name: 'Units',
    selector: 'units',
    sortable: false,
    maxWidth:20,
    wrap:true,
    grow:1
  },
  {
    name: 'Source',
    selector: 'source',
    wrap:true,
    sortable: true
  },
  {
    name: 'boundID',
    selector: 'boundID',
    omit:true,
  }
];


const StyledDescription = styled.div`
  font-size: 14px;
  color: ${props => props.theme.labelColorLT};
  line-height: 18px;
  margin-bottom: 12px;
`;

const InputForm = styled.div`
  flex-grow: 1;
  padding: 32px;
  background-color: ${props => props.theme.panelBackgroundLT};
`;

const StyledInput = styled.input`
  width: 100%;
  padding: ${props => props.theme.inputPadding};
  color: ${props => (props.error ? 'red' : props.theme.titleColorLT)};
  height: ${props => props.theme.inputBoxHeight};
  border: 0;
  outline: 0;
  font-size: ${props => props.theme.inputFontSize};

  :active,
  :focus,
  &.focus,
  &.active {
    outline: 0;
  }
`;

const StyledFromGroup = styled.div`
  margin-top: 30px;
  display: flex;
  flex-direction: row;
`;

export const StyledInputLabel = styled.div`
  font-size: 11px;
  color: ${props => props.theme.textColorLT};
  letter-spacing: 0.2px;
  ul {
    padding-left: 12px;
  }
`;

export const StyledError = styled.div`
  color: red;
`;

export const StyledErrorDescription = styled.div`
  font-size: 14px;
  font-weight: bold;
`;


const Error = ({error, url}) => (
  <StyledError>
    <StyledErrorDescription>{url}</StyledErrorDescription>
    <StyledErrorDescription>{error.message}</StyledErrorDescription>
  </StyledError>
);

class LoadCuratedMap extends Component {
  state = {
    dataUrl: '',
    tVar: 'No Selection',
    cVar: 'GLB_ADM0',
    filteredData: data.filter(item => item.boundID && item.boundID == ("GLB_ADM0"))
  };

  onMapUrlChange = e => {
    // TODO: validate url
    this.setState({
      dataUrl: e.target.value
    });
  };

  onLoadCuratedMap = () => {
    const {dataUrl} = this.state;
    if (!dataUrl) {
      return;
    }

    this.props.onLoadCuratedMap({dataUrl});
  };


onFormChange = (event, value) => {
  console.log(value.code);
  this.setState({filteredData: data.filter(item => item.boundID && item.boundID == (value.code))})
}

  render() {
    return (
      <div>
        <InputForm>
          <StyledDescription>
            <FormattedMessage id="Choose one or more of our curated datasets to load.  Data will be aggregated to the region and spatial granularity you choose. All of our data is provided freely, and only require acknowledgement to use.  Acknowledgements should include a link to this (www.geodesc.org) website." />
          </StyledDescription>
          <StyledFromGroup>

            <Autocomplete
                id="choose-a-region"
                options={regionOptions}
                getOptionLabel={(option) => option.label}
                //onChange={"(event, value) => this.setState({tVar: value})"}
                onChange={(event, value) => this.onFormChange(event, value)}
                
                
                style={{ width: "100%" }}
                renderInput={(params) => <TextField {...params} label="Choose a Region (Showing Data Available for Global ADM0 - Countries)" variant="outlined" />}
            />

          </StyledFromGroup>
          {this.props.error && <Error error={this.props.error}/>}
        </InputForm>
        <DataTable
        noHeader={true}
        columns={columns}
        data={this.state.filteredData}
        defaultSortField="title"
        selectableRows={true}
        selectableRowsNoSelectAll={true}
        selectableRowsHighlight={true}
        selectableRowsVisibleOnly={false}
        highlightOnHover={true}
        striped={true}
        persistTableHead={true}
        pagination={true}
      />
      <StyledFromGroup>
      <Button>Add Selected Data</Button>
      </StyledFromGroup>
      </div>
    );
  }
}

LoadCuratedMap.propTypes = propTypes;

export default LoadCuratedMap;
