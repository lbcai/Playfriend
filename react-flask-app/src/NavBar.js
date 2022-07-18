import { NavLink } from "react-router-dom";
import './NavBar.css';
import icon from './images/pf_icon_vector.svg';
import github from './images/GitHub-Mark.svg';
import { scroller } from 'react-scroll';

function NavBar() {

  const handleClick_gitHub = () => {
    window.open("https://github.com/lbcai/Playfriend");
  };

  const scrollToFeatures = () => {
    scroller.scrollTo('features', {
      duration: 500,
      delay: 0,
      smooth: "easeInOutQuart",
    });
  };

  const scrollToGameLog = () => {
    scroller.scrollTo('game-log', {
      duration: 500,
      delay: 0,
      smooth: "easeInOutQuart",
    });
  };

  const scrollToContact = () => {
    scroller.scrollTo('contact', {
      duration: 500,
      delay: 0,
      smooth: "easeInOutQuart",
    });
  };

  const scrollToTop = () => {
    scroller.scrollTo('navBackground', {
        duration: 500,
        delay: 0,
        smooth: "easeInOutQuart",
      });
  }

  return (
    <nav className='navBackground'>

        <img className='logo' src={ icon } alt="Playfriend Logo" onClick={ scrollToTop } />

        <NavLink
            className={({ isActive }) =>
            isActive ? 'active navBox': 'inactive navBox'}
            exact="true" to="/features" onClick={ scrollToFeatures }>Features</NavLink>

        <NavLink
            className={({ isActive }) =>
            isActive ? 'active navBox': 'inactive navBox'}
            exact="true" to="/gamelog" onClick={ scrollToGameLog }>Game Log</NavLink>

        <NavLink
            className={({ isActive }) =>
            isActive ? 'active navBox': 'inactive navBox'}
            exact="true" to="/manual">Manual</NavLink>

        <NavLink
            className={({ isActive }) =>
            isActive ? 'active navBox': 'inactive navBox'}
            exact="true" to="/contact" onClick={ scrollToContact }>Contact</NavLink>

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
