import "../App.css";
import { useState } from "react";
import axios from "axios";

export default function Result(url) {
  const [isLoading, setIsLoading] = useState(true);
  const [imageUrl, setImageUrl] = useState("");

  async function generateImage() {
    const code = new URLSearchParams(window.location.search).get("code");
    let responseCode = {
      code: code,
    };
    await axios.post("/api/registerToken", responseCode);
    await axios
      .get("/api/getImage")
      .then((Response) => setImageUrl(Response.data));

    setIsLoading(false);
  }

  if (isLoading) {
    generateImage();
  } else {
    return (
      <div>
        <img
          style={{ width: 512, height: 512 }}
          src={imageUrl}
          alt="Your mood!"
        />
      </div>
    );
  }
}
