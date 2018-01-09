import React from 'react';
import Highlighter from 'react-highlight-words';
import WordWeights from './WordWeights';
import {NewTabLink} from "./util";
import './PageResults.css';
import MissingTokens from "./MissingTokens";

const Page = ({data}) => (
  <div className="Page" data-uuid={data.uuid}>
    <NewTabLink className="Page-link" href={data.url}>
      <div className="Page-title">{data.title}</div>
      <div className="Page-url">{data.url}</div>
      <Highlighter className="Page-content" searchWords={data.preview.highlight}
                   autoEscape={true} textToHighlight={data.preview.preview}/>
    </NewTabLink>
    <MissingTokens description="Missing" weights={data.tfidf}/>
    <WordWeights weights={data.tfidf} description="TF-IDF weights for this document" isOpened={false} />
  </div>
);

class PageResults extends React.Component {
  render() {
    const {results} = this.props;

    return (
      <div className="PageResults">
        {results.map((data) => (
          <Page key={data.uuid} data={data}/>
        ))}
      </div>
    );
  }
}

export default PageResults;
