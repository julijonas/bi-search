import React from "react";
import "./MissingTokens.css";

class MissingTokens extends React.Component {
  render() {
    const {weights, description} = this.props;
    const missing = Object.keys(weights).filter((word) => weights[word] === 0);

    if (!missing.length) {
      return null;
    }

    return (
      <div className="MissingTokens">
        {description}:{missing.map((word) => (
          <React.Fragment key={word}>
            {' '}<s>{word}</s>
          </React.Fragment>
        ))}
      </div>
    );
  }
}

export default MissingTokens;
