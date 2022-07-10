import { NavLink } from "react-router-dom";
import './NavBar.css';
import icon from './images/pf_icon_vector.svg';
import github from './images/GitHub-Mark.svg';

function NavBar() {

  const handleClick_gitHub = () => {
    window.open("https://github.com/lbcai/Playfriend");
  };

  return (
    <nav className='navBackground'>

        <img className='logo' src={ icon } alt="Playfriend Logo" />

        <NavLink
            className={({ isActive }) =>
            isActive ? 'active navBox': 'inactive navBox'}
            exact="true" to="/features">Features</NavLink>

        <NavLink
            className={({ isActive }) =>
            isActive ? 'active navBox': 'inactive navBox'}
            exact="true" to="/log">Game Log</NavLink>

        <NavLink
            className={({ isActive }) =>
            isActive ? 'active navBox': 'inactive navBox'}
            exact="true" to="/manual">Manual</NavLink>

        <NavLink
            className={({ isActive }) =>
            isActive ? 'active navBox': 'inactive navBox'}
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
