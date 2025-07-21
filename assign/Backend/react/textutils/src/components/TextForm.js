import React, { useState } from "react";

export default function TextForm(Props) {
  const handleUpClick = () => {
    console.log("Uppercase was clicked" + text);
    let newText = text.toUpperCase();
    setText(newText);
  };
  const handleOnChange = (event) => {
    console.log("On change");
    setText(event.target.value);
  };
  const [text, setText] = useState("Enter text here");
  // console.log(useState("enter text here2"))
  return (
    <>
      <div>
        <div className="mb-3">
          <label htmlFor="myBox" class="form-label">
            {Props.heading}
          </label>
          <textarea
            className="form-control"
            onChange={handleOnChange}
            id="myBox"
            value={text}
            rows="8"
          ></textarea>
        </div>
        <button className="btn btn-primary" onClick={handleUpClick}>
          Convert the Upper case
        </button>
      </div>
      <div className="container">
        <h1>Your text summary</h1>
        <p>{text.split(" ").length} and {text.length}</p>
      </div>
    </>
  );
}
