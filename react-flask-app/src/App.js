/* import { Route, Switch } from "react-router-dom"; */
import NavBar from './NavBar';
import './App.css';
import logoCircle from './images/pf_icon_complete.svg';
import textShort from './images/pf_text_short.svg';
import textLong from './images/pf_text.svg';
import 'animate.css';


function App() {
  return (
    <div className="App">

      <NavBar />

      <div className='animate__animated splat hero'>
        <img className='animate__animated animate__rollIn animate__faster App-logo' src={ logoCircle } alt="Playfriend Logo" />
        <img className='animate__animated textPop App-logo-text' src={ textShort } alt="Playfriend Logo" />
        <img className='animate__animated mask animate__faster App-logo-text' src={ textLong } alt="Playfriend Logo" />
      </div>

      <div className='App-header-div'>
      <header className="App-header">
          A bot for chatroom minigames!
        </header>
        <button> Invite to Server </button>
      </div>

      <div className='content'>
        <p>Text text here try now demo </p>
        <button> Demo </button>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
        <p>test</p>
      </div>

    </div>
  );
}

export default App;
