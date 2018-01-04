import React from 'react';
import Collapse from 'react-collapse';
import './WordScorePanel.css';

const WordScore = ({wordscore}) => (
   <p className="Box">
     <div className="PercentageBox" style={{width: '' + wordscore.split(',')[1]*10 + '%'}}>
      <div className="Word">{wordscore.split(',')[0]}:</div> 
      <div className="Score">{wordscore.split(',')[1]}</div>
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
    const {results, isOpened} = this.props;
    const isChecked = this.state.isOpened;
    return (
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
                  {results.map(function(result){
                     return <WordScore wordscore={result} key={result.split(',')[0]} />
                  })}
              </div>
           </Collapse>
        </div>
    )
  }
}

export default WordScorePanel;

