import { Route, Routes } from "react-router-dom";
import NavBar from './NavBar';
import './App.css';
import 'animate.css';
import Main from './Main';
import Manual from './Manual';

function App() {
  return (
    <div className="App">
      <NavBar />
      <div className="contain">
        <Routes>
          <Route path="/" element={<Main />} />
          <Route exact path="/manual" element={<Manual />} />
          <Route path="*" element={<Main />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
