import React from 'react';
import logo from './logo.svg';
import './App.css';
import SearchBox from './SearchBox';
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
      firstTime: !query,
      loading: !!query,
      mode: mode || 'slides', // Default mode
      query: query || '',
      feedbackTerms: [],
      smart: 'ltclnc'.split(''), // Default smart scheme
      results: [],
      queryWeights: {},
      selected: [],
      page: 0,
      pageCount: 0,
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

  handleParamChange = (params, performQuery, clearResults=false) => {
    if (performQuery) {
      params = {firstTime: false, selected: [], feedbackTerms: [], ...params,
        query: (params.query || this.state.query).trim()};
      if (clearResults) {
        params = {...params, page: 0, results: [], loading: true};
      }
      const state = {...this.state, ...params};
      this.fetchResults(state);
      this.updateTitle(state);
      window.history.pushState(state, '', `/${state.mode}/${state.query}`);
    }
    this.setState(params);
  };

  handleSearchChange = (params, performQuery) => {
    this.handleParamChange(params, performQuery, true);
  };

  updateTitle({query}) {
    window.document.title = (query ? `${query} - ` : '') + 'Informatics Search';
  }

  updateState(changes) {
    // Save state both in React and history
    window.history.replaceState({...this.state, ...changes}, '', null);
    this.setState(changes);
  }

  fetchResults({mode, query, feedbackTerms, smart, page}) {
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
      this.updateState({...results, loading: false});
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
      results, selected, page, pageCount, queryWeights} = this.state;

    let content;

    if (loading) {
      content = (
        <div class="App-loader">Loading</div>
      )
    } else if (!firstTime) {
      if (results.length) {

        if (mode === 'slides') {

          content = (
            <div>
              {feedbackTerms.length ? (
                <SlideFeedback terms={feedbackTerms}
                               onUpdate={this.handleFeedbackUpdate} onRemove={this.handleTermRemove}/>
              ) : null}
              <SlideResults results={results} selected={selected} onSelect={this.handleSlideSelect}/>
              <Pagination page={page} pageCount={pageCount} onChange={this.handleParamChange}/>
            </div>
          );

        } else {

          content = (
            <div>
              <PageResults results={results} queryWeights={queryWeights}/>
              <Pagination page={page} pageCount={pageCount} onChange={this.handleParamChange}/>
            </div>
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
          <SearchBox query={query} smart={smart} mode={mode} onChange={this.handleSearchChange}/>
          {content}
        </div>
      </div>
    );
  }
}

export default App;

