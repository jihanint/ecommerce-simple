import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav>
      <Link to="/">Products</Link>
      <Link to="/cart">Cart</Link>
      <Link to="/login">Login</Link>
      <Link to="/register">Register</Link>
    </nav>
  );
}

export default Navbar;
