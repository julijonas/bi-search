import React from 'react';
import Collapse from 'react-collapse';
import './WordScorePanel.css';

const WordScore = ({word, score}) => (
   <p className="Box">
     <div className="PercentageBox" style={{width: '' + score*100 + '%'}}>
      <div className="Word">{word}:</div>
      <div className="Score">{score.toFixed(3)}</div>
     </div>
   </p>
);

class WordScorePanel extends React.Component {

  constructor(props) {
     super(props);
     this.state = {
       isOpened: this.props.isOpened
     };
     this.handleChange = this.handleChange.bind(this);
  }

  handleChange() {
     this.setState({isOpened: !this.state.isOpened});
  }

  render() {
    const {results} = this.props;
    const isChecked = this.state.isOpened;
    return results ? (
        <div className="WordScore">
           <label className="label">
              <input className="input"
               type="checkbox"
               checked={isChecked}
               onChange={this.handleChange} />
             Show TFIDF
           </label>
      
           <Collapse isOpened={isChecked} fixedHeight={results.length*36} >
              <div className="WordWithScore">
                  {Object.keys(results).map(function(key, index){
                     return <WordScore word={key} score={results[key]} key={key} />
                  })}
              </div>
           </Collapse>
        </div>
    ) : null
  }
}

export default WordScorePanel;
