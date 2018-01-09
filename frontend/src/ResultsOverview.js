import React from 'react';
import './ResultsOverview.css';
import MissingTokens from "./MissingTokens";
import WordWeights from "./WordWeights";

class ResultsOverview extends React.Component {
  render() {
    const {page, resultCount, weights} = this.props;

    return (
      <div className="ResultsOverview">
        <div className="ResultsOverview-count">
          {page === 0 ? 'A' : `Page ${page + 1} of a`}bout {resultCount.toLocaleString()} results
        </div>
        <MissingTokens description="Tokens not in index" weights={weights}/>
        <WordWeights weights={weights} description="overall TF-IDF weights" isOpened={false} />
      </div>
    );
  }
}

export default ResultsOverview;
