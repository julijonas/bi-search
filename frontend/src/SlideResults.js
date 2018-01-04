import React from 'react';
import "./SlideResults.css";

const Slide = ({data, selected, onSelect}) => (
  <div className={"Slide" + (selected ? " Slide-selected" : "")} data-uuid={data.uuid}>
    <a className="Slide-selection" onClick={onSelect}>
      {selected ? "−" : "+"}
    </a>
    <a className="Slide-link" href={data.url} target="_blank">
      <img className="Slide-thumb" src={data.thumb} alt={data.title}/>
      <div className="Slide-score">{data.score.toFixed(3)}</div>
      <div className="Slide-title">{data.title}</div>
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
