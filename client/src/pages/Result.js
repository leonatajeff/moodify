import "./css/Result.css";
import { useState } from "react";
import axios from "axios";
import { saveAs } from "file-saver";
import { JellyTriangle } from "@uiball/loaders";
import { TypeAnimation } from "react-type-animation";
import { Gallery } from "react-grid-gallery";

import {
  TwitterShareButton,
  TwitterIcon,
  RedditShareButton,
  RedditIcon,
  PinterestShareButton,
  PinterestIcon,
} from "react-share";

export default function Result() {
  const [isLoading, setIsLoading] = useState(true);
  const [imageUrl, setImageUrl] = useState("");
  const [images, setImages] = useState(() => {
    return fetchUserImages();
  });

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

  async function fetchUserImages() {
    let imageData = [];
    const images = await axios.get("/api/userImages");
    const rawImageUrls = images.data["imagePath"];
    // imageArray contains path names /image/username.png relative to https://storage.googleapis.com/cs1520moodify.appspot.com

    for (let i = 0; i < rawImageUrls.length; i++) {
      const fullUrl =
        "https://storage.googleapis.com/cs1520moodify.appspot.com" +
        rawImageUrls[i];
      imageData.push({ src: fullUrl });
    }
    console.log(imageData);
    setImages(imageData);
  }

  const downloadImage = () => {
    saveAs(imageUrl, "image.jpg"); // Put your image url here.
    console.log("Image downloaded");
  };

  if (isLoading) {
    generateImage();
    return (
      <div className="result" style={{ marginTop: "164px" }}>
        <JellyTriangle size={60} speed={1.75} color="white" />
        <TypeAnimation
          sequence={[
            "Generating visuals.....", // Types 'One'
            1000, // Waits 1s
            () => {
              console.log("Done typing!"); // Place optional callbacks anywhere in the array
            },
          ]}
          wrapper="div"
          cursor={true}
          repeat={Infinity}
          style={{ fontSize: "2em", marginTop: "10px" }}
        />
      </div>
    );
  } else {
    return (
      <div className="result">
        <h1> Your recent songs visualized! </h1>
        <img
          style={{ width: 512, height: 512 }}
          src={imageUrl}
          alt="Your mood!"
        />
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
          {images.length > 0 ? (
            <div className="past-moods-container">
              <text className="past-moods-header"> Past moods </text>
              <Gallery images={images} enableImageSelection={false} />
            </div>
          ) : (
              ''
          )}
        </div>
      </div>
    );
  }
}
