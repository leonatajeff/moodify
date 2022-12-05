export default function Donate() {
    return (
        <div className="donate">
            <h1 className="donate-header"> Donate to Moodify </h1> 
            <p className="donate-text">
                Moodify is a free service that is open source and free to use.
                We are a small team of developers and we are working hard to
                make Moodify better every day. If you would like to support us,
                you can donate to us through the link below.
            </p>    
            <button className="donate-btn" href="https://www.paypal.com/donate?hosted_button_id=ZT2ZQZQZQZQZQ">
                <text className="donate-text"> Send Fake Money </text>
            </button>
        </div>
    );
}