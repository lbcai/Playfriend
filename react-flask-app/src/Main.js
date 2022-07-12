import logoCircle from './images/pf_icon_complete.svg';
import textShort from './images/pf_text_short.svg';
import textLong from './images/pf_text.svg';

function Main() {

    const handleClick_invite = () => {
        window.open("https://discord.com/oauth2/authorize?client_id=785345529722175498&permissions=470080&scope=bot");
      };

    const handleClick_demo = () => {
    window.open("https://discord.com/oauth2/authorize?client_id=785345529722175498&permissions=470080&scope=bot");
    };

    return (
        <div>
            <div className='animate__animated splat hero'>
                <img className='animate__animated animate__rollIn animate__faster App-logo' src={ logoCircle } alt="Playfriend Logo" />
                <img className='animate__animated textPop App-logo-text' src={ textShort } alt="Playfriend Logo" />
                <img className='animate__animated mask animate__faster App-logo-text' src={ textLong } alt="Playfriend Logo" />
            </div>

            <div className='App-header-div'>
            <header className="App-header">
                A bot for chatroom minigames!
                </header>
                <button onClick={handleClick_invite}> Invite to Server </button>
            </div>

            <div className='content'>
                <div className='content-div-left'>
                    <p>Playfriend is a chat bot that allows members of your server to play minigames together.
                        New minigames are currently in development and feature suggestions are welcome.</p>
                    <p>Playfriend will also include random generators, helpful chat features, and more.</p>

                    <p>Try out Playfriend with a demo!</p>
                    <button onClick={handleClick_demo}> Demo </button>
                </div>

                <div className='content-div-left'>
                    <p>test</p>
                </div>
            </div>

            <div className='content'>
                <p>Features</p>
            </div>

            <div className='content'>
                <p>Game Log</p>
            </div>

            <div className='content'>
                <p>Contact</p>
            </div>

        </div>
    );
}

export default Main;
