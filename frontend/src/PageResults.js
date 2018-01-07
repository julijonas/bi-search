import React from 'react';
import './PageResults.css';
import WordScorePanel from './WordScorePanel';

var Highlighter = require('react-highlight-words');

const Page = ({data, preview}) => (
  <div className="Page" data-uuid={data.uuid}>
    <a className="Page-link" href={data.url} target="_blank"> 
      <div className="Page-title">{data.title}</div>
      <div className="Page-url">{data.url}</div>
      <div className="Page-content"><Highlighter
        highlightClassName="Highlight"
        searchWords={preview.highlight}
        autoEscape={true}
        textToHighlight={preview.preview}/>
      </div>
    </a>
    <WordScorePanel results={data.tfidf} text="Show TFIDF" isOpened={false} />
  </div>
);

const QueryWords = ({queryWeights}) => (
  <div className="QueryWords">
    <WordScorePanel results={queryWeights} text="Show TFIDF weights for query words" isOpened={false} />
  </div>
);

class PageResults extends React.Component {

  render() {
    const {results, queryWeights} = this.props;
    return (
      <div className="PageResults">
        <QueryWords queryWeights={queryWeights}/>
        {results.map((data) => (
          <Page key={data.uuid} data={data} preview={data.preview}/>
        ))}
      </div>
    )
  }
}

export default PageResults;
