import { NavLink, useLocation } from "react-router-dom";
import './NavBar.css';
import icon from './images/pf_icon_vector.svg';
import github from './images/GitHub-Mark.svg';
import { scroller } from 'react-scroll';
import { useEffect, useState, useRef } from 'react';

function NavBar() {

  const [dropdown, setDropdown] = useState(false);
  const dropdownRef = useRef();
  const buttonRef = useRef();

  let location = useLocation();


  useEffect(() => {
    if (location.pathname === '/') {
      scrollToTop();
    } else {
      scrollToX(location.pathname.slice(1));
    }

  }, [location]);

  // monitor if click outside of dropdown in mobile mode
  useEffect(() => {
    const clickOutside = (e) => {
      if (!dropdownRef.current.contains(e.target) && !buttonRef.current.contains(e.target)) {
        setDropdown(false);
      }
    };
    window.addEventListener("mousedown", clickOutside);

    return(() => {
      document.removeEventListener("mousedown", clickOutside);
    })
  }, []);

  const handleClick_gitHub = () => {
    window.open("https://github.com/lbcai/Playfriend");
  };

  const scrollToX = (string) => {
    scroller.scrollTo(string, {
      offset: -60,
      duration: 500,
      delay: 0,
      smooth: "easeInOutQuart",
    });
  };

  const scrollToTop = () => {
    scroller.scrollTo('App', {
        duration: 500,
        delay: 0,
        smooth: "easeInOutQuart",
      });
  }

  return (
    <nav className='navBackground'>

        <NavLink className="logo-link" to="/" exact="true"><img className='logo' src={ icon } alt="Playfriend Logo"/></NavLink>
      <div className={`hider ${dropdown ? "dropdown" : ""}`} ref={dropdownRef}>
        <NavLink
            className={({ isActive }) =>
            isActive ? 'isactive navBox': 'inactive navBox'}
            exact="true" to="/features">Features</NavLink>

        <NavLink
            className={({ isActive }) =>
            isActive ? 'isactive navBox': 'inactive navBox'}
            exact="true" to="/game-log">Game Log</NavLink>

        <NavLink
            className={({ isActive }) =>
            isActive ? 'isactive navBox': 'inactive navBox'}
            exact="true" to="/manual">Manual</NavLink>

        <NavLink
            className={({ isActive }) =>
            isActive ? 'isactive navBox': 'inactive navBox'}
            exact="true" to="/contact">Contact</NavLink>

        <NavLink
            className={({ isActive }) =>
            isActive ? 'inactive navBox gitHubLink': 'inactive navBox gitHubLink'}
            exact="true" to="#" onClick={ handleClick_gitHub }>
              <img className='gitHubLogo' src={ github } alt="GitHub Logo" />
              GitHub</NavLink>
      </div>
        <button className="burger" onClick={() => setDropdown(!dropdown)} ref={buttonRef}>
          <div className="burger-bar bar-1"></div>
          <div className="burger-bar bar-2"></div>
          <div className="burger-bar bar-3"></div>
        </button>
    </nav>
  );
}

export default NavBar;
