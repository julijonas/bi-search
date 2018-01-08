import React from 'react';
import Highlighter from 'react-highlight-words';
import WordScorePanel from './WordScorePanel';
import {NewTabLink} from "./util";
import './PageResults.css';

const Page = ({data}) => (
  <div className="Page" data-uuid={data.uuid}>
    <NewTabLink className="Page-link" href={data.url}>
      <div className="Page-title">{data.title}</div>
      <div className="Page-url">{data.url}</div>
      <div className="Page-content"><Highlighter
        highlightClassName="Highlight"
        searchWords={data.preview.highlight}
        autoEscape={true}
        textToHighlight={data.preview.preview}/>
      </div>
    </NewTabLink>
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
          <Page key={data.uuid} data={data}/>
        ))}
      </div>
    );
  }
}

export default PageResults;
