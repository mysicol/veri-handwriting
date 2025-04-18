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

  const imageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setForm({ image: file });
    }
  };

  let sendForm = async function () {
    const form_data = new FormData()
    form_data.append("image", form.image)

    let result = await axios.post("/api/image", form_data);
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
          <div className="summary most-legible">
            <h2>Least Legible:</h2> {summary.mostLegible}
          </div>
          <div className="summary most-legible">
            <h2>Most Legible:</h2> {summary.mostConsistent}
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
        		<p className="apple-text">Get started by submitting a photo of your handwriting! <i>(one letter per box)</i></p>
			<div id="form">
                {/* <input id="phrase" type="text"></input> */}
                <label for="file-upload-button" class="input-buttons">Upload image</label>
            		<input type="file" id="file-upload-button" onChange={imageUpload} />
            		<img src={form.image} />
                <label for="submit-button" class="input-buttons">Submit</label>
            		<button id="submit-button" className="submit-button" onClick={sendForm}>
        		Submit
        		</button>
		</div>
	   </div>
      	</div>
    </div>
  );

  return <>{formSent ? summaryPage : formPage}</>;
}
