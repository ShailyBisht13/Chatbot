import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import { Icon, Logo } from "../components/homeicons";
import "./auth.css";

export default function Signup() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPass, setShowPass] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const signup = async () => {
    if (!email || !password) {
      alert("Email and password required");
      return;
    }

    setLoading(true);
    try {
      await axios.post("http://localhost:5000/auth/signup", {
        email,
        password,
      });

      alert("Account created successfully. Please login.");
      navigate("/login");
    } catch (err) {
      alert(err.response?.data?.error || "Signup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <form
        className="auth-card"
        noValidate
        onSubmit={(e) => {
          e.preventDefault();
          signup();
        }}
      >
        <Link to="/" className="auth-brand" aria-label="Deepshiva home">
          <Logo />
          <span>
            <strong>Deepshiva</strong>
            <small>Spiritual Tourism &amp; Himalayan Wisdom</small>
          </span>
        </Link>

        <h2>Sign Up</h2>
        <p className="auth-sub">Create an account to save your chats and continue anywhere.</p>

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
            placeholder="Create Password"
            autoComplete="new-password"
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
          {loading ? "Please wait..." : "Create Account"}
        </button>

        <p className="auth-switch">
          Already have an account?{" "}
          <Link to="/login" className="auth-link">
            Login
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