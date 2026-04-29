import { useState } from "react";
import "../styles/Auth.css";

function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="container">
      <div className="form-box">
        <h1>{isLogin ? "Login" : "Register"}</h1>

        <form>
          {!isLogin && (
            <div className="input-group">
              <label>Full Name</label>
              <input type="text" placeholder="Enter your full name" />
            </div>
          )}

          <div className="input-group">
            <label>Email</label>
            <input type="email" placeholder="Enter your email" />
          </div>

          <div className="input-group">
            <label>Password</label>
            <input type="password" placeholder="Enter your password" />
          </div>

          {!isLogin && (
            <div className="input-group">
              <label>Confirm Password</label>
              <input type="password" placeholder="Confirm your password" />
            </div>
          )}

          <button type="submit" className="btn">
            {isLogin ? "Login" : "Register"}
          </button>
        </form>

        <p className="toggle-text">
          {isLogin
            ? "Don't have an account?"
            : "Already have an account?"}

          <span onClick={() => setIsLogin(!isLogin)}>
            {isLogin ? " Register" : " Login"}
          </span>
        </p>
      </div>
    </div>
  );
}

export default AuthPage;