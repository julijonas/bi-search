import React from "react";
import "./Modal.css";

export default class Modal extends React.Component {
  handleClose = ({target}) => {
    if (target === this.rootRef) {
      this.props.onClose();
    }
  };

  handleEsc = ({key}) => {
    if (key === "Escape") {
      this.props.onClose();
    }
  };

  componentDidMount(){
    document.addEventListener("keydown", this.handleEsc);
  }

  componentWillUnmount(){
    document.removeEventListener("keydown", this.handleEsc);
  }

  render() {
    const {onClose, children} = this.props;

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
