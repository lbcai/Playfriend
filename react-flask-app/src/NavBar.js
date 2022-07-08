import { NavLink } from "react-router-dom";
import './NavBar.css';

function NavBar() {
  return (
    <nav className='navBackground'>
        <ul>
            <li>
                <NavLink
                    className={({ isActive }) =>
                    isActive ? 'active' : 'inactive'
                    }
                    exact="true" to="/features">Features</NavLink>
            </li>
            <li>
                <NavLink
                    className={({ isActive }) =>
                    isActive ? 'active' : 'inactive'
                    }
                    exact="true" to="/log">Game Log</NavLink>
            </li>
            <li>
                <NavLink
                    className={({ isActive }) =>
                    isActive ? 'active' : 'inactive'
                    }
                    exact="true" to="/contact">Contact</NavLink>
            </li>
        </ul>
    </nav>
  );
}

export default NavBar;
