import React from 'react';
import Collapse from 'react-collapse';
import './WordScorePanel.css';

const WordScore = ({word, score}) => (
  <div className="WordScore" style={{width: `${score * 100}%`}}>
    <div className="WordScore-score">{word}: {score.toFixed(3)}</div>
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
    const {results, text} = this.props;

    return (
      <div className="WordScorePanel">
        <a onClick={this.handleChange} className="WordScorePanel-toggle">
          {this.state.isOpened ? 'Hide' : 'Show'} {text}
        </a>

        <Collapse isOpened={this.state.isOpened} fixedHeight={results.length * 36} >
          <div className="WordScorePanel-scores">
            {Object.keys(results).map((key) => (
               <WordScore word={key} score={results[key]} key={key} />
            ))}
          </div>
        </Collapse>
      </div>
    );
  }
}

export default WordScorePanel;
