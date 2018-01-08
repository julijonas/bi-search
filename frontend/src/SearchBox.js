import React from 'react';
import Modal from "./Modal";
import {NewTabLink} from "./util";
import './SearchBox.css';


const SmartLetter = ({name, value, options, onChange}) => (
  <span className="SmartLetter">
    <select className="SmartLetter-select" name={name} onChange={onChange} value={value}>
      {Object.entries(options).map(([option, description]) => (
        <option key={option}>{option} ({description})</option>
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
  {
    n: 'natural',
    l: 'logarithm',
    a: 'augmented',
    b: 'boolean',
    L: 'log average',
  },
  {
    n: 'no',
    t: 'idf',
    p: 'prob idf',
  },
  {
    n: 'none',
    c: 'cosine',
    b: 'byte size',
  },
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
      smartInfoShown: false,
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

  showSmartInfo = () => {
    this.setState({smartInfoShown: true});
  };

  hideSmartInfo = () => {
    this.setState({smartInfoShown: false});
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
          <div className="SearchBox-smart-title">Weighting scheme:</div>
          <SmartBox value={smart} options={[...smartOptions, ...smartOptions]} onChange={this.handleSmartChange} />
          <button className="SearchBox-smart-info" onClick={this.showSmartInfo}>?</button>
        </div>
        <Modal show={this.state.smartInfoShown} onClose={this.hideSmartInfo}>
          <h2>SMART weighting schemes</h2>
          <p>
            See also Wikipedia entries on <NewTabLink href="https://en.wikipedia.org/wiki/SMART_Information_Retrieval_System">
            SMART Information Retrieval System</NewTabLink> and <NewTabLink href="https://en.wikipedia.org/wiki/Relevance_feedback">
            relevance feedback</NewTabLink>.
          </p>
        </Modal>
      </div>
    )
  }
}

export default SearchBox;
