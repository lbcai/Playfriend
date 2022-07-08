import { NavLink } from "react-router-dom";
import './NavBar.css';
import icon from './images/pf_icon_vector.svg';

function NavBar() {
  return (
    <nav className='navBackground'>
        <div className='navDiv'>
        <img className='logo' src={ icon } alt="Playfriend Logo" />
        </div>

        <div className='navDiv'>
            <NavLink
                className={({ isActive }) =>
                isActive ? 'active' : 'inactive'
                }
                exact="true" to="/features">Features</NavLink>
        </div>
        <div className='navDiv'>
            <NavLink
                className={({ isActive }) =>
                isActive ? 'active' : 'inactive'
                }
                exact="true" to="/log">Game Log</NavLink>
        </div>
        <div className='navDiv'>
            <NavLink
                className={({ isActive }) =>
                isActive ? 'active' : 'inactive'
                }
                exact="true" to="/contact">Contact</NavLink>
        </div>
    </nav>
  );
}

export default NavBar;
