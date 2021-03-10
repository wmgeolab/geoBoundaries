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

import {PanelHeaderFactory, Icons} from 'kepler.gl/components';
import {BUG_REPORT_LINK, USER_GUIDE_DOC} from 'kepler.gl/constants';
import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

export function CustomPanelHeaderFactory(...deps) {
  const PanelHeader = PanelHeaderFactory(...deps);
  const defaultActionItems = PanelHeader.defaultProps.actionItems;

  const LogoTitle = styled.div`
  display: inline-block;
  margin-left: 6px;
`;

  const LogoName = styled.div`
    .logo__link {
      color: #F0B323;
      font-size: 14px;
      font-weight: 600;
      letter-spacing: 1.17px;
    }
  `;
  const LogoVersion = styled.div`
    font-size: 10px;
    color: ${props => props.theme.subtextColor};
    letter-spacing: 0.83px;
    line-height: 14px;
  `;

  const LogoWrapper = styled.div`
    display: flex;
    align-items: flex-start;
  `;

  const LogoSvgWrapper = styled.div`
    margin-top: 3px;
  `;

  const LogoSvg = () => (
    <svg className="side-panel-logo__logo" width="22px" height="15px" viewBox="0 0 22 15">
 <g>
 <rect fill="#fff" opacity="0.0" id="canvas_background" height="17" width="24" y="-1" x="-1"/>
  <g display="none" overflow="visible" y="0" x="0" height="100%" width="100%" id="canvasGrid">
   <rect fill="url(#gridpattern)" strokeWidth="0" y="0" x="0" height="100%" width="100%"/>
  </g>
 </g>
 <g>
 <ellipse stroke="#ffffff" ry="7.63158" rx="7.63158" id="svg_2" cy="7.45504" cx="13.23684" strokeWidth="1.5" fill="#64ccc9"/>
  <ellipse stroke="#ffffff" ry="7.63158" rx="4.38597" id="svg_4" cy="7.45504" cx="17.35965" strokeWidth="1.5" fill="#64ccc9"/>
 </g>
    </svg>
  );

  const KeplerGlLogo = ({appName, appWebsite = KEPLER_GL_WEBSITE, version}) => (
    <LogoWrapper className="side-panel-logo">
      <LogoSvgWrapper>
        <LogoSvg />
      </LogoSvgWrapper>
      <LogoTitle className="logo__title">
        <LogoName className="logo__name">
          <a className="logo__link" target="_blank" rel="noopener noreferrer" href="http://www.geodesc.org">
            geoDesc
          </a>
        </LogoName>
        {version ? <LogoVersion className="logo__version">0.01a</LogoVersion> : null}
      </LogoTitle>
    </LogoWrapper>
  );

  KeplerGlLogo.propTypes = {
    appName: PropTypes.string,
    version: PropTypes.oneOfType([PropTypes.string, PropTypes.bool]),
    appWebsite: PropTypes.string
  };


  PanelHeader.defaultProps = {
    ...PanelHeader.defaultProps,
    appName: "geodesc",
    appWebsite: "http://www.geodesc.org",
    version: "0.1a",
    logoComponent: KeplerGlLogo,
    actionItems: [
      {
        id: 'bug',
        iconComponent: Icons.Bug,
        href: "https://github.com/wmgeolab/geoBoundaries/issues/new?template=geoDesc_bug.md",
        blank: true,
        tooltip: 'Bug Report',
        onClick: () => {}
      },
      {
        id: 'docs',
        iconComponent: Icons.Docs,
        href: "http://geoboundaries.org/help/",
        blank: true,
        tooltip: 'User Guide',
        onClick: () => {}
      },
      //defaultActionItems.find(item => item.id === 'storage'),
      {
        ...defaultActionItems.find(item => item.id === 'save'),
        label: null,
        tooltip: 'Share'
      }
    ]
  };
  return PanelHeader;
}

CustomPanelHeaderFactory.deps = PanelHeaderFactory.deps;

export function replacePanelHeader() {
  return [PanelHeaderFactory, CustomPanelHeaderFactory];
}
