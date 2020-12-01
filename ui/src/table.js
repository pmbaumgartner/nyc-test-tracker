import React from 'react';
import Papa from 'papaparse';
import { HEADERS } from './const.js';

class Header extends React.Component {
  render() {
    return (
      <div className="table-header">
        <table>
          <tr>
            {HEADERS.map((d, i) => {
              return (
                <td className="headers" key={'col ' + i}>
                  {d}
                </td>
              )
            })}
          </tr>
        </table>
      </div>
    )
  }
}


class Body extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      data: []
    }

    this.getData = this.getData.bind(this);
  }

  componentWillMount() {
    this.getCsvData();
  }

  fetchCsv() {
    return fetch('/data/latest.csv').then(function (response) {
      let reader = response.body.getReader();
      let decoder = new TextDecoder('utf-8');

      return reader.read().then(function (result) {
        return decoder.decode(result.value);
      });
    });
  }

  getData(result) {
    this.setState({ data: result.data });
  }

  async getCsvData() {
    let csvData = await this.fetchCsv();

    Papa.parse(csvData, {
      complete: this.getData
    });
  }

  render() {
    return (
      <div className="section-body">
        <table className="section-body-table">
          <tbody>
            {this.state.data.slice(1).map((d, i) => {
              // last line of csv is empty, len == 1
              if (d.length > 1) {
                return (<tr>
                  <td key={'col ' + i + 1}>
                    {d[1]}
                  </td>
                  <td key={'col ' + i + 2}>
                    {d[2]}
                  </td>
                  <td key={'col ' + i + 3}>
                    {d[3]}
                  </td>
                  <td key={'col ' + i + 4}>
                    {d[4]}
                  </td>
                </tr>
                )
              }
            })}
          </tbody>
        </table>
      </div >
    );
  }
}


class WaitTimes extends React.Component {
  render() {
    return (
      <div className="section">
        <Header />
        <Body />
      </div>
    )
  }
}
export default WaitTimes