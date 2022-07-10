import { NavLink } from "react-router-dom";
import './NavBar.css';
import icon from './images/pf_icon_vector.svg';

function NavBar() {
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

    </nav>
  );
}

export default NavBar;
