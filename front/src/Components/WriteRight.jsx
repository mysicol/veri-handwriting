import { useState } from "react";
import axios from "axios";
import "./WriteRight.css";

export default function WriteRight() {
  let [form, setForm] = useState({ image: "" });
  let [formSent, setFormSent] = useState(false);
  let [summary, setSummary] = useState({
    text: "",
    neatness: 0,
    consistency: 0,
    mostLegible: "",
    mostConsistent: "",
    worst: [
      {
        id: 0,
        letter: "",
        score: 0,
      },
    ],
  }); // default data

  let sendForm = async function () {
    let result = await axios.post("/api/image", form);
    console.log(result.data.summary);
    setSummary(result.data.summary);
    setForm({ image: "" });
    setFormSent(true);
  };

  let summaryPage = (
    <div id="statistics">
      <h1 className="header">Here are your statistics!</h1>
      <div className="content">
        <div className="feedback">
          <div className="summary">
            <h2>Summary:</h2>
            <div>{summary.text}</div>
          </div>
          <div className="scores">
            <h3>Score:</h3>
            <div className="neatness">Neatness: {summary.neatness}%</div>
            <div className="consistency">
              Consistency: {summary.consistency}%
            </div>
          </div>
          <div className="worst">
            <h3>Letters to work on:</h3>
            <table className="worst-list">
              <tr>
                <th>Letter</th>
                <th>Legibility</th>
              </tr>
              {summary.worst.map(({ id, letter, score }) => (
                <tr key={id} className="worst-item">
                  <td>{letter}</td>
                  <td>{score}%</td>
                </tr>
              ))}
            </table>
          </div>
        </div>
        <div className="special">
          <div className="most-legible">
            Most Legible: {summary.mostLegible}
          </div>
          <div className="most-consistent">
            Most Consistent: {summary.mostConsistent}
          </div>
        </div>
      </div>
    </div>
  );

  let formPage = (
    <div className="form-container">
	  <div className="apple-container">
	  	<h1 className="header">WriteRight</h1>
	  	<div className="apple-text-container">
        		<h2 className="apple-text">Welcome to WriteRight</h2>
        		<h2 className="apple-text">Get started by submitting a photo of</h2>
	  		<h2 className="apple-text">your beautiful handwriting!</h2>
        		<h3 className="apple-text">**Try to keep only one letter per box :)</h3>
			<div id="form">
            		<input type="file" />
            		<img src={form.image} />
            		<button className="submit-button" onClick={sendForm}>
        		Submit
        		</button>
		</div>
	   </div>
      	</div>
    </div>
  );

  return <>{formSent ? summaryPage : formPage}</>;
}
