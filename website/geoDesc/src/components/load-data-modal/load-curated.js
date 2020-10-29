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

const regionOptions = [
    { code: 'GLBADM0', label: 'Global / ADM0 (Countries)'},
    { code: 'GLBADM0', label: 'Global / ADM1 (States)'},
    { code: 'GLBADM0', label: 'Global / ADM2 (Variable)'},
    { code: 'AFG-ADM1', label: 'Afghanistan / ADM1 (Province)'},
    { code: 'AFG-ADM2', label: 'Afghanistan / ADM2 (District)'},
    { code: 'ITA-ADM1', label: 'Italy / ADM1 (Region)'},
    { code: 'ITA-ADM2', label: 'Italy / ADM2 (Provinces)'}
];


const data = [{ id: 1, title: 'DatasetA', year: 'Test' },
            {id:2, title:"DatasetB", year:'test2'}
];
const columns = [
  {
    name: 'Title',
    selector: 'title',
    sortable: true,
  },
  {
    name: 'Test',
    selector: 'year',
    sortable: true,
    right: true,
  },
];


const propTypes = {
  onLoadCuratedMap: PropTypes.func.isRequired
};





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
    cVar: 'No Selection'
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

  onSelectCountry = () => {
    this.setState({cVar: this.state.tVar.code})
    console.log(this.state.tVar)
    console.log(this.state.tVar.code)
    console.log(this.state.tVar.label)
  };

  render() {
    return (
      <div>
        <InputForm>
          <StyledDescription>
            <FormattedMessage id="Choose one of our curated datasets to load.  All of our data is provided freely, and only require acknowledgement to use.  Acknowledgements should include a link to this (www.geodesc.org) website." />
          </StyledDescription>
          <StyledFromGroup>

            <Autocomplete
                id="choose-a-region"
                options={regionOptions}
                getOptionLabel={(option) => option.label}
                onChange={(event, value) => this.setState({tVar: value})}
                style={{ width: "100%" }}
                renderInput={(params) => <TextField {...params} label="Choose a Region" variant="outlined" />}
            />

            <Button type="submit" cta size="small" onClick={this.onSelectCountry}>
              <FormattedMessage id="Explore Datasets" />
            </Button>
            
            <StyledDescription>
                <FormattedMessage id={this.state.cVar}></FormattedMessage>
            </StyledDescription>
          </StyledFromGroup>
          {this.props.error && <Error error={this.props.error}/>}
        </InputForm>
        <DataTable
        title="Arnold Movies"
        columns={columns}
        data={data}
      />
      </div>
    );
  }
}

LoadCuratedMap.propTypes = propTypes;

export default LoadCuratedMap;
