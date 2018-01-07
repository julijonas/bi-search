import React from 'react';
import './SearchBox.css';


const SmartLetter = ({name, value, options, onChange}) => (
  <span className="SmartLetter">
    <select className="SmartLetter-select" name={name} onChange={onChange} value={value}>
      {options.map((option) => (
        <option key={option}>{option}</option>
      ))}
    </select>
  </span>
);


class SmartBox extends React.Component {

  handleChange = ({target}) => {
    const triple = this.props.value.slice();
    triple[target.name] = target.value;
    this.props.onChange(triple);
  };

  render() {
    const {value, options} = this.props;
    return (
      <span>
        {options.map((options, index) => (
          <SmartLetter key={index} name={index} value={value[index]} onChange={this.handleChange} options={options}/>
        ))}
      </span>
    );
  }
}


const smartOptions = [
  ['n', 'l', 'a', 'b', 'L'],
  ['n', 't', 'p'],
  ['n', 'c', 'u', 'b'],
];


const offers = [
  'bayes rule',
  'dna vs rna',
  'sql injection',
  'apples oranges',
  'merge sort',
  'inverted index',
  'map reduce',
];


class SearchBox extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      offer: offers[Math.floor(Math.random() * offers.length)],
    };
  }

  handleQueryChange = ({target}) => {
    this.props.onChange({query: target.value}, false);
  };

  handleEnter = ({key}) => {
    if (key === 'Enter') {
      // This is the default action
      this.props.onChange({mode: 'slides'}, true);
    }
  };

  handleModeChange = ({target}) => {
    this.props.onChange({mode: target.name}, true);
  };

  handleSmartChange = (smart) => {
    this.props.onChange({smart}, true);
  };

  render() {
    const {query, smart} = this.props;
    return (
      <div className="SearchBox">
        <div className="SearchBox-params">
          <input className="SearchBox-query" value={query}
                 onChange={this.handleQueryChange} onKeyPress={this.handleEnter}
                 minLength="3" placeholder={`Try: ${this.state.offer}`}/>
          <button className="SearchBox-button" name="slides" onClick={this.handleModeChange}>Slides</button>
          <button className="SearchBox-button" name="pages" onClick={this.handleModeChange}>Pages</button>
        </div>
        <div className="SearchBox-smart">
          <SmartBox value={smart} options={[...smartOptions, ...smartOptions]} onChange={this.handleSmartChange} />
          <a className="SearchBox-smart-info" title="What's this?"
             href="https://en.wikipedia.org/wiki/SMART_Information_Retrieval_System">?</a>
        </div>
      </div>
    )
  }
}

export default SearchBox;
