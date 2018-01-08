import React from "react";
import "./Modal.css";

export default class Modal extends React.Component {
  handleClose = ({target}) => {
    if (target === this.rootRef) {
      this.props.onClose();
    }
  };

  render() {
    const {show, onClose, children} = this.props;

    if (!show) {
      return null;
    }

    return (
      <div className="Modal" onClick={this.handleClose}
           ref={(rootRef) => {this.rootRef = rootRef;}}>
        <div className="Modal-content">
          <a className="Modal-close" onClick={onClose}>✕</a>
          {children}
        </div>
      </div>
    );
  }
}
