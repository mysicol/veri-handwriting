import { useState } from "react";
import axios from "axios";
import "./WriteRight.css";

export default function WriteRight() {
  let [form, setForm] = useState({ image: null });
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
    setForm({ image: null });
    setFormSent(true);
  };

  let summaryPage = (
    <div id="statistics">
      <h1 className="header">Here are your statistics!</h1>
      <div className="content">
        <div className="feedback">
        <div className="summary">
            <h3>What you Entered:</h3>
            <div>{summary.input}</div>
          </div>
          <div className="summary">
            <h3>Summary:</h3>
            <div>{summary.text}</div>
          </div>
          <div className="summary">
            <h3>Score:</h3>
            <div className="neatness">Neatness: {summary.neatness}%</div>
            <div className="consistency">
              Consistency: {summary.consistency}%
            </div>
          </div>
          <div className="summary">
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
        		<p className="apple-text">Get started by submitting a photo of your beautiful handwriting! **Try to keep only one letter per box :)</p>
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
