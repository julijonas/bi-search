import React from 'react';
import logo from './logo.svg';
import './App.css';
import SearchBox from './SearchBox';
import ResultsOverview from './ResultsOverview';
import PageResults from './PageResults';
import SlideFeedback from './SlideFeedback';
import SlideResults from './SlideResults';
import Pagination from './Pagination';

export const backendUrl = process.env.NODE_ENV === 'production' ? '/' : `//${window.location.hostname}:5000/`;


class App extends React.Component {

  constructor(props) {
    super(props);

    // Parsing URL if there is no history.state
    let mode, query;
    if (!window.history.state) {
      const urlParams = decodeURIComponent(window.location.pathname).split('/');
      if (urlParams.length === 3 && ['slides', 'pages'].includes(urlParams[1])) {
        [, mode, query] = urlParams;
      }
    }

    // Restore history.state or initialize from URL or from scratch
    this.state = window.history.state || {
      // Loading flags
      firstTime: !query,
      loading: !!query,

      // Parameters
      mode: mode || 'slides', // Default mode
      query: (query || '').trim(),
      smart: 'ltclnc'.split(''), // Default smart scheme
      page: 0,
      selected: [],
      feedbackTerms: [],

      // Results
      results: [],
      queryWeights: {},
      pageCount: 0,
      resultCount: 0,
    };

    // Fetch results if restored from URL
    if (!window.history.state && query) {
      this.fetchResults(this.state);
    }

    window.onpopstate = ({state}) => {
      this.updateTitle(state);
      this.setState(state);
    };
  }

  handleParamChange = (params, performQuery) => {
    const query = (params.query || this.state.query).trim();
    if (query && performQuery) {
      params = {
        firstTime: false,
        loading: true,
        page: 0,
        feedbackTerms: [],
        selected: [],
        results: [],
        queryWeights: {},
        pageCount: 0,
        resultCount: 0,
        ...params,
        query};
      const state = {...this.state, ...params};
      this.fetchResults(state);
      this.updateTitle(state);
      window.history.pushState(state, '', `/${state.mode}/${state.query}`);
    }
    this.setState(params);
  };

  updateTitle({query}) {
    window.document.title = (query ? `${query} - ` : '') + 'Informatics Search';
  }

  updateState(changes) {
    // Save state both in React and history
    window.history.replaceState({...this.state, ...changes}, '', null);
    this.setState(changes);
  }

  fetchResults(params) {
    const {mode, query, feedbackTerms, smart, page} = params;
    fetch(`${backendUrl}search/${mode}`, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: [query, ...feedbackTerms.map(({term}) => term)].join(' '),
        smart: smart.join(''),
        page: page,
      }),
    }).then((res) => {
      return res.json();
    }).then((results) => {
      if (this.state.loading) {
        this.updateState({...params, ...results, loading: false});
      }
    }).catch(e => {
      console.error("Failed: ", e);
    });
  }

  handleSlideSelect = (uuid) => {
    const index = this.state.selected.indexOf(uuid);
    let selected;
    if (index !== -1) {
      selected = this.state.selected.slice();
      selected.splice(index, 1);
    } else {
      selected = [...this.state.selected, uuid];
    }
    this.updateState({selected});
    if (selected.length) {
      this.fetchFeedbackTerms({...this.state, selected});
    } else {
      this.updateState({feedbackTerms: []});
    }
  };

  fetchFeedbackTerms({query, selected, smart}) {
    fetch(`${backendUrl}search/feedback`, {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: query,
        docs: selected,
        smart: smart.join(''),
      }),
    }).then((res) => {
      return res.json()
    }).then((feedbackTerms) => {
      this.updateState({feedbackTerms});
    }).catch(e => {
      console.error("Failed: ", e);
    });
  }

  handleFeedbackUpdate = () => {
    this.setState({loading: true});
    this.fetchResults(this.state);
  };

  handleTermRemove = (index) => {
    const feedbackTerms = this.state.feedbackTerms.slice();
    feedbackTerms.splice(index, 1);
    this.updateState({feedbackTerms})
  };

  render() {
    const {loading, firstTime, mode, query, feedbackTerms, smart,
      results, selected, page, pageCount, resultCount, queryWeights} = this.state;

    let content;

    if (loading) {
      content = (
        <div className="App-loader">Loading</div>
      )
    } else if (!firstTime) {
      if (results.length) {

        if (mode === 'slides') {

          content = (
            <React.Fragment>
              {feedbackTerms.length ? (
                <SlideFeedback terms={feedbackTerms}
                               onUpdate={this.handleFeedbackUpdate} onRemove={this.handleTermRemove}/>
              ) : null}
              <ResultsOverview page={page} resultCount={resultCount} weights={queryWeights}/>
              <SlideResults results={results} selected={selected} onSelect={this.handleSlideSelect}/>
              <Pagination page={page} pageCount={pageCount} onChange={this.handleParamChange}/>
            </React.Fragment>
          );

        } else {

          content = (
            <React.Fragment>
              <ResultsOverview page={page} resultCount={resultCount} weights={queryWeights}/>
              <PageResults results={results} queryWeights={queryWeights}/>
              <Pagination page={page} pageCount={pageCount} onChange={this.handleParamChange}/>
            </React.Fragment>
          );

        }
      } else {
        content = (
          <h2>No results found.</h2>
        );
      }
    }

    return (
      <div className="App">
        <header className="App-header">
          <a href="/">
            <img src={logo} className="App-logo" alt="logo" />
            <h1 className="App-title">Informatics Search</h1>
          </a>
        </header>
        <div className="App-content">
          <SearchBox query={query} smart={smart} mode={mode} onChange={this.handleParamChange}/>
          {content}
        </div>
      </div>
    );
  }
}

export default App;

