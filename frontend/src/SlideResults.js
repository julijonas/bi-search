import React from 'react';
import {backendUrl} from './App';
import {NewTabLink} from "./util";
import "./SlideResults.css";

const Slide = ({data, selected, onSelect}) => (
  <div className={"Slide" + (selected ? " Slide-selected" : "")} data-uuid={data.uuid}>
    <a className="Slide-selection" onClick={onSelect}>
      {selected ? "−" : "+"}
    </a>
    <NewTabLink className="Slide-link" href={data.url}>
      <div className="Slide-score">Score of this slide: {data.score.toFixed(3)}</div>
      <img className="Slide-thumb" src={`${backendUrl}static/thumbs/${data.uuid}.png`} alt={data.title}/>
    </NewTabLink>
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
        <div className="SlideResults-title">Mark the relevant documents to refine your query:</div>
        {results.map((data) => (
          <Slide key={data.uuid} data={data} selected={selected.includes(data.uuid)} onSelect={this.handleSelect}/>
        ))}
      </div>
    )
  }
}

export default SlideResults;
