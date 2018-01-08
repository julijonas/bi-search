import React from "react";
import "./Modal.css";

const Modal = ({show, onClose, children}) => {
  if (!show) {
    return null;
  }

  return (
    <div className="Modal">
      <div className="Modal-content">
        <a className="Modal-close" onClick={onClose}>✕</a>
        {children}
      </div>
    </div>
  );
};

export default Modal;
