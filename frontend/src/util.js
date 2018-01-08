import React from "react";

export const NewTabLink = (props) => (
  <a target="_blank" rel="noopener noreferrer" {...props}>{props.children}</a>
);
