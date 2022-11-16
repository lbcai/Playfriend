import { NavLink, useLocation } from "react-router-dom";
import './NavBar.css';
import icon from './images/pf_icon_vector.svg';
import github from './images/GitHub-Mark.svg';
import { scroller } from 'react-scroll';
import { useEffect } from 'react';

function NavBar() {

  let location = useLocation();

  useEffect(() => {
    scrollToX(location.pathname.slice(1));
  }, [location]);


  const handleClick_gitHub = () => {
    window.open("https://github.com/lbcai/Playfriend");
  };

  const scrollToX = (string) => {
    scroller.scrollTo(string, {
      duration: 500,
      delay: 0,
      smooth: "easeInOutQuart",
    });
  };

  return (
    <nav className='navBackground'>

        <NavLink className="logo-link" to="/" exact="true"><img className='logo' src={ icon } alt="Playfriend Logo"/></NavLink>

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

    </nav>
  );
}

export default NavBar;
