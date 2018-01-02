import React from 'react';
import "./PageResults.css";

const WordScore = ({wordscore}) => (
  <div className="WordScore">
    <p>Word: {wordscore.split(',')[0]} Score: {wordscore.split(',')[1]}</p>
  </div>
);

const Page = ({data}) => (
  <div className="Page" data-uuid={data.uuid}>
    <a className="Page-link" href={data.url} target="_blank"> 
      <div className="Page-title">{data.title}</div>
      <div className="Page-url">{data.url}</div>
      <div className="Page-content">{data.content}</div>
   </a>
   {data.tfidf.map(function(result){
       return <WordScore wordscore={result} key={result.split(',')[0]}/>
   })} 
  </div>
);

class PageResults extends React.Component {

  handleSelect = ({target}) => {
    this.props.onSelect(target.parentElement.dataset.uuid);
  };

  render() {
    const {results, selected} = this.props;
    return (
      <div className="PageResults">
        {results.map((data) => (
          <Page key={data.uuid} data={data}/>
        ))}
      </div>
    )
  }
}

export default PageResults;
