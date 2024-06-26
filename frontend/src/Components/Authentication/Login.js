import React, { useState } from "react";
import "./components/LoginFP.css";
import { database } from "../../Components/firebase";
import { ref, push, child, update } from "firebase/database";
import { Link, useNavigate } from "react-router-dom";
import ParticlesBg from "particles-bg";
import BackButton from "../BackButton";
import axios from "axios";
import { FaRegEye, FaRegEyeSlash } from "react-icons/fa6";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loginText, setLoginText] = useState("");
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const [emailFocused, setEmailFocused] = useState(false);
  const [passwordFocused, setPasswordFocused] = useState(false);
  const [passwordVisible, setPasswordVisible] = useState(false);

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    if (id === "email") {
      setEmail(value);
    }
    if (id === "password") {
      setPassword(value);
    }
  };

  // let validate = Yup.object().shape({
  //   email: Yup.string().required().email(),
  //   password: Yup.string().required().min(6),
  // });

  // let data = [
  //   {
  //     label: "email",
  //     id: 1,
  //     placeholder: "Email",
  //   },
  //   {
  //     label: "password",
  //     id: 2,
  //     placeholder: "Password",
  //     type: "password",
  //   },
  // ];

  const handleBack = () => {
    navigate("/");
  };

  const handleSubmit = async () => {
    let obj = {
      email: email,
      password: password,
    };
    console.log(obj);
    setIsLoading(true);
    axios
    .post(
      `${process.env.REACT_APP_PROTOCOL}://${process.env.REACT_APP_DOMAIN}${process.env.REACT_APP_PORT}/api/login/`,
      obj,
      {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      }
    )
    .then((response) => {
      setIsLoading(false);
    })
    .catch(() => {
      setIsLoading(false);
      alert("Server error! Please check the input and try again. If the error persists, refer to the docs! ");
    });
    // const newPostKey = push(child(ref(database), "posts")).key;
    // const updates = {};
    // updates["/" + newPostKey] = obj;
    // setLoginText("Welcome!");
    // return update(ref(database), updates);
  };

  return (
    <div className="auth-container">
      <ParticlesBg type="cobweb" bg={true} />
      <div style={{ position: "absolute", top: 50, left: 50 }}>
        <BackButton handleBack={handleBack} arrowColor={"#EEE"} color={"black"}></BackButton>
      </div>

      {/* <div className="wrapper">
        <h1>Login</h1>
        <AppForm
          data={data}
          onSubmit={handleSubmit}
          handleInputChange={handleInputChange}
          validationSchema={validate}
        ></AppForm>
        <div className="forgot-password">
          <a href="#">Forgot Password</a>
        </div>
       
        <div className="signup-link">
          <p>
            Don't Have an account? <Link to="/register">Register</Link>
          </p>
        </div>
      </div> */}

      <div className="wrapper">
        <form>
          <h1>Login</h1>
          <div className="input-box">
            <i className="fas fa-user icon"></i>
            <input
              type="email"
              id="email"
              className="form__input"
              value={email}
              onFocus={() => setEmailFocused(true)}
              onBlur={() => setEmailFocused(false)}
              onChange={handleInputChange}
              required
            />
            <label className={emailFocused || email ? "focused-textInput" : ""} htmlFor="email">
              Email
            </label>
          </div>
          <div className="input-box">
            <i className="fas fa-lock icon"></i>
            <input
              className="form__input"
              type={!passwordVisible ? "password" : "text"}
              id="password"
              value={password}
              minLength={8}
              onFocus={() => setPasswordFocused(true)}
              onBlur={() => setPasswordFocused(false)}
              onChange={handleInputChange}
              required
            />
            <label className={passwordFocused || password ? "focused-textInput" : ""} htmlFor="password">
              Password
            </label>
            <div
              style={{ position: "absolute", right: 10, top: 10 }}
              onClick={() => {
                setPasswordVisible(!passwordVisible);
              }}
            >
              {passwordVisible ? <FaRegEye size={20} /> : <FaRegEyeSlash size={20} />}
            </div>
          </div>
          <div className="forgot-password">
            <a href="#">Forgot Password</a>
          </div>
          <button onClick={handleSubmit} type="submit" className="btn">
            Login
          </button>
          <div className="signup-link">
            <p>
              Don't Have an account? <Link to="/register">Register</Link>
            </p>
          </div>
        </form>
        {loginText && <p style={{ textAlign: "center", marginTop: "20px" }}>{loginText}</p>}
      </div>
    </div>
  );
}

export default Login;
