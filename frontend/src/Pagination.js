import React from 'react';
import './Pagination.css';


class Pagination extends React.Component {

  goBack = () => {
    if (this.props.page > 0) {
      this.props.onChange({page: this.props.page - 1}, true);
    }
  };

  goForward = () => {
    if (this.props.page < this.props.pageCount - 1) {
      this.props.onChange({page: this.props.page + 1}, true);
    }
  };

  render() {
    const {page, pageCount} = this.props;
    return (
      <div className="Pagination">
        <a className="Pagination-back" onClick={this.goBack}>«</a>
        <span className="Pagination-current">page {page + 1} / {pageCount}</span>
        <a className="Pagination-forward" onClick={this.goForward}>»</a>
      </div>
    );
  }
}

export default Pagination;
