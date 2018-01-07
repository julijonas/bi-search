import React from 'react';
import "./SlideResults.css";
import { backendUrl } from './App';

const Slide = ({data, selected, onSelect}) => (
  <div className={"Slide" + (selected ? " Slide-selected" : "")} data-uuid={data.uuid}>
    <a className="Slide-selection" onClick={onSelect}>
      {selected ? "−" : "+"}
    </a>
    <a className="Slide-link" href={data.url} target="_blank">
      <div className="Slide-title">{data.title}</div>
      <div className="Slide-score">{data.score.toFixed(3)}</div>
      <img className="Slide-thumb" src={`${backendUrl}static/thumbs/${data.uuid}.png`} alt={data.title}/>
    </a>
  </div>
);

class SlideResults extends React.Component {

  handleSelect = ({target}) => {
    this.props.onSelect(target.parentElement.dataset.uuid);
  };

  render() {
    const {results, selected} = this.props;
    return (
      <div className="SlideResults">
        {results.map((data) => (
          <Slide key={data.uuid} data={data} selected={selected.includes(data.uuid)} onSelect={this.handleSelect}/>
        ))}
      </div>
    )
  }
}

export default SlideResults;
