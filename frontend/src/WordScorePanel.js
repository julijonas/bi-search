import React from 'react';
import Collapse from 'react-collapse';
import './WordScorePanel.css';

const WordScore = ({word, score}) => (
  <div className="WordScore" style={{width: `${score * 100}%`}}>
    <div className="WordScore-score">{word}:&nbsp;{score.toFixed(3)}</div>
  </div>
);

class WordScorePanel extends React.Component {

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
    const {results, text, missingText} = this.props;

    const missing = Object.keys(results).filter((word) => results[word] === 0);
    const available = Object.keys(results).filter((word) => results[word] > 0);

    return (
      <div className="WordScorePanel">
        {missing.length ? (
          <div className="WordScorePanel-missing">{missingText}:{missing.map((word) => (
            <React.Fragment>
              {' '}<s>{word}</s>
            </React.Fragment>
          ))}
          </div>
        ) : null}

        <a onClick={this.handleChange} className="WordScorePanel-toggle">
          {this.state.isOpened ? 'Hide' : 'Show'} {text}
        </a>

        <Collapse isOpened={this.state.isOpened}>
          <div className="WordScorePanel-scores">
            {available.map((word) => (
               <WordScore word={word} score={results[word]} key={word} />
            ))}
          </div>
        </Collapse>
      </div>
    );
  }
}

export default WordScorePanel;
