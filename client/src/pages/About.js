export default function About() {
  return (
    <div className="about">
      <article>
        <h3>
          Moodify uses your monthly listens to generate AI-powered art through
          DALL-E.
        </h3>
        <br />
        Inspired by Receiptify Created by Jefferson Leonata, Alex Gelbavicius,
        Daniel Sawyer, Zipan Huang.
      </article>
      <button
        className="code-button"
        href="https://github.com/leonatajeff/moodify"
      >
        <text className="code-text"> Check out our code! </text>
      </button>
    </div>
  );
}
