import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { Icon, Logo } from "../components/homeicons";
import "./auth.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const login = async () => {
    if (!email.trim() || !password.trim()) {
      alert("Please enter both email and password.");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post("http://localhost:5000/auth/login", {
        email: email.trim(),
        password: password.trim(),
      });

      if (res.data && res.data.token) {
        localStorage.setItem("token", res.data.token);
        localStorage.setItem("user", JSON.stringify(res.data.user || { email }));
        navigate("/chat");
      } else {
        alert("Login failed: Invalid server response");
      }
    } catch (err) {
      console.error("Login request error:", err);
      alert(err.response?.data?.error || "Login failed. Please ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <form
        className="auth-card"
        onSubmit={(e) => {
          e.preventDefault();
          login();
        }}
      >
        <Link to="/" className="auth-brand" aria-label="Deepshiva home">
          <Logo />
          <span>
            <strong>Deepshiva</strong>
            <small>Spiritual Tourism &amp; Himalayan Wisdom</small>
          </span>
        </Link>

        <h2>Login</h2>
        <p className="auth-sub">Welcome back. Sign in to continue your journey.</p>

        <label className="auth-field">
          <span className="auth-field-icon">{Icon.mail(20)}</span>
          <input
            type="email"
            placeholder="Email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>

        <label className="auth-field">
          <span className="auth-field-icon">{Icon.lock(20)}</span>
          <input
            type={showPass ? "text" : "password"}
            placeholder="Password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button
            type="button"
            className="auth-eye"
            onClick={() => setShowPass((v) => !v)}
            aria-label={showPass ? "Hide password" : "Show password"}
          >
            {showPass ? Icon.eyeoff(20) : Icon.eye(20)}
          </button>
        </label>

        <button type="submit" className="auth-btn" disabled={loading}>
          {loading ? "Please wait..." : "Login"}
        </button>

        <p className="auth-switch">
          New user?{" "}
          <Link to="/signup" className="auth-link">
            Sign up
          </Link>
        </p>

        <div className="auth-divider"><span>or</span></div>

        <Link to="/chat" className="auth-guest">
          Continue as Guest {Icon.arrow(18)}
        </Link>
      </form>
    </div>
  );
}