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
      <div className="Page-content">
        <Highlighter
          highlightClassName="Highlight" searchWords={data.preview.highlight}
          autoEscape={true} textToHighlight={data.preview.preview}/>
      </div>
    </NewTabLink>
    <WordScorePanel results={data.tfidf} missingText="Missing"
                    text="TF-IDF term weights for this document" isOpened={false} />
  </div>
);

class PageResults extends React.Component {
  render() {
    const {results, queryWeights} = this.props;

    return (
      <div className="PageResults">
        <WordScorePanel results={queryWeights} missingText="Tokens not in index"
                        text="overall TF-IDF term weights" isOpened={false} />
        {results.map((data) => (
          <Page key={data.uuid} data={data}/>
        ))}
      </div>
    );
  }
}

export default PageResults;
