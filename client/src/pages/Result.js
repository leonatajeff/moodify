import "./css/Result.css";
import { useState } from "react";
import axios from "axios";
import { saveAs } from "file-saver";
import {
  TwitterShareButton,
  TwitterIcon,
  RedditShareButton,
  RedditIcon,
  PinterestShareButton,
  PinterestIcon,
} from "react-share";

export default function Result(url) {
  const [isLoading, setIsLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState("");
  const [displaySentence, setDisplaySentence] = useState("");

  async function generateImage() {
    const code = new URLSearchParams(window.location.search).get("code");
    let responseCode = {
      code: code,
    };
    await axios.post("/api/registerToken", responseCode);
    await axios
      .get("/api/getImage")
      .then((Response) => setImageUrl(Response.data));

    console.log(displaySentence);
    setDisplaySentence("Your music has been surreal and emotional");
    setIsLoading(false);
  }

  const downloadImage = () => {
    saveAs(imageUrl, "image.jpg"); // Put your image url here.
    console.log("Image downloaded");
  };

  if (isLoading) {
    generateImage();
  } else {
    return (
      <div className="result">
        <img
          style={{ width: 512, height: 512 }}
          src={imageUrl}
          alt="Your mood!"
        />
        <h1> Your music has been surreal and emotional </h1>
        <div className="share-container">
          <text className="share-message">
            {" "}
            Share your mood with your friends!{" "}
          </text>
          <button className="share-button" onClick={downloadImage}>
            Download your image as a JPG
          </button>
          <div className="social-container">
            <TwitterShareButton
              className="social-icon"
              url={imageUrl}
              title="Check out my mood!"
            >
              <TwitterIcon size={32} round={true} />
            </TwitterShareButton>
            <RedditShareButton
              className="social-icon"
              url={imageUrl}
              title="Check out my mood!"
            >
              <RedditIcon size={32} round={true} />
            </RedditShareButton>
            <PinterestShareButton
              className="social-icon"
              url={imageUrl}
              title="Check out my mood!"
            >
              <PinterestIcon size={32} round={true} />
            </PinterestShareButton>
          </div>
        </div>
      </div>
    );
  }
}
