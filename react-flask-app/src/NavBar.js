import { NavLink } from "react-router-dom";
import './App.css';

function NavBar() {
  return (
    <nav>
        <ul>
            <li>
                <NavLink
                    className={({ isActive }) =>
                    isActive ? activeClassName : undefined
                    }
                    exact="true" to="/">Home</NavLink>
            </li>
            <li>
                <NavLink
                    className={({ isActive }) =>
                    isActive ? activeClassName : undefined
                    }
                    exact="true" to="/log">Game Log</NavLink>
            </li>
            <li><NavLink
                    className={({ isActive }) =>
                    isActive ? activeClassName : undefined
                    }
                    exact="true" to="/contact">Contact</NavLink></li>
        </ul>
    </nav>
  );
}

export default NavBar;
