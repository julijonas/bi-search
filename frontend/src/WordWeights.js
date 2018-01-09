import React from 'react';
import Collapse from 'react-collapse';
import './WordWeights.css';

const WordScore = ({word, score}) => (
  <div className="WordScore" style={{width: `${score * 100}%`}}>
    <div className="WordScore-score">{word}:&nbsp;{score.toFixed(3)}</div>
  </div>
);

class WordWeights extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      isOpened: this.props.isOpened,
    };
  }

  handleChange = () => {
    this.setState({isOpened: !this.state.isOpened});
  };

  render() {
    const {weights, description} = this.props;

    const available = Object.keys(weights).filter((word) => weights[word] > 0);

    return (
      <div className="WordWeights">
        <a onClick={this.handleChange} className="WordWeights-toggle">
          {this.state.isOpened ? 'Hide' : 'Show'} {description}
        </a>

        <Collapse isOpened={this.state.isOpened}>
          {available.map((word) => (
            <WordScore word={word} score={weights[word]} key={word} />
          ))}
        </Collapse>
      </div>
    );
  }
}

export default WordWeights;
