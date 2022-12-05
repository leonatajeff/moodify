import "../App.css";
import axios from "axios";
import Result from "./Result";

// 'URLSearchParams(window.location.search)' will get url string after the '?' & .get() will get the code value from the url
const code = new URLSearchParams(window.location.search).get("code");

export default function Home() {
  const handleLogin = async () => {
    const loginUrl = await axios.get("/api/authorize");
    window.location.href = loginUrl.data["auth_endpoint"];
  };

  return (
    <div className="generation">
      <h1 className="moodify-header"> Moodify, visualize your listening history with Artifical Intelligence </h1>
      {code ? (
        <Result />
      ) : (
        <button className="spotify-button" onClick={handleLogin}>
          <text className="login-text"> Login with Spotify </text>
        </button>
      )}
    </div>
  );
}
