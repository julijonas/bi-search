import React from 'react';
import "./SlideFeedback.css";


const Term = ({term, weight, onRemove, index}) => (
  <div className="Term" data-index={index}>
    <span className="Term-term">{term}</span>
    <span className="Term-weight">{weight.toFixed(3)}</span>
    <a className="Term-remove" onClick={onRemove}>✕</a>
  </div>
);


class SlideFeedback extends React.Component {

  onRemove = ({target}) => {
    this.props.onRemove(target.parentElement.dataset.index);
  };

  render() {
    const {terms, onUpdate} = this.props;
    return (
      <div className="SlideFeedback">
        <div className="SlideFeedback-terms">
          {terms.map(({term, weight}, index) => (
            <Term key={term} index={index} term={term} weight={weight} onRemove={this.onRemove} />
          ))}
        </div>
        <button className="SlideFeedback-update" onClick={onUpdate}>Update</button>
      </div>
    );
  }
}

export default SlideFeedback;
