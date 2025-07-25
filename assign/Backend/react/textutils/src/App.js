import "./App.css";
import Navbar from "./components/Navbar";
import TextForm from "./components/TextForm";

function App() {
  return (
    <>
      <Navbar title="TextUtils" aboutText="about text" />
      <div className="container">
        <TextForm heading="Enter your Text to analyze" />
      </div>
    </>
  );
}

export default App;
