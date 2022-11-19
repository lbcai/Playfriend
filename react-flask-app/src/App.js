import { Route, Routes } from "react-router-dom";
import NavBar from './NavBar';
import './App.css';
import 'animate.css';
import Main from './Main';
import Manual from './Manual';
import { scroller } from 'react-scroll';
import { useEffect, useState } from 'react';

function App() {

  const [topVisible, setTopVisible] = useState(false);

  const scrollToTop = () => {
    scroller.scrollTo('App', {
        duration: 500,
        delay: 0,
        smooth: "easeInOutQuart",
      });
  }

  useEffect(() => {
    const toggle = () => {
      const scroll = document.documentElement.scrollTop;
      if (scroll > 10) {
        setTopVisible(true);
      } else if (scroll <= 10) {
        setTopVisible(false);
      };
    };
    document.addEventListener("scroll", toggle);

    return(() => {
      document.removeEventListener("scroll", toggle);
    })
  }, []);


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
      <button className={`to-top ${topVisible ? "" : "show-top"}`} onClick={() => scrollToTop()}><div className="up">ˆ</div></button>
    </div>
  );
}

export default App;
