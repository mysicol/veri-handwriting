import { useState } from "react";
import axios from "axios";
import "./WriteRight.css";

export default function WriteRight() {
  let [form, setForm] = useState({ image: "test" });
  let [formSent, setFormSent] = useState(false);
  let [summary, setSummary] = useState({
    score: 0,
  }); // default data

  let sendForm = async function () {
    let result = await axios.post("/api/image", form);
    console.log(result.data.summary);
    setSummary(result.data.summary);
    setForm({ image: "" });
    setFormSent(true);
  };

  let summaryPage = (
    <div className="summary-container">
      <div id="summary">
        <h1 className="header">Write Right</h1>
        <div className="score">Score: {summary.score}%</div>
      </div>
    </div>
  );

  let formPage = (
    <div className="form-container">
      <div id="form">
        <h1>Submit Image</h1>
        <button className="submit-button" onClick={sendForm}>
          Submit
        </button>
      </div>
    </div>
  );

  return <>{formSent ? summaryPage : formPage}</>;
}
