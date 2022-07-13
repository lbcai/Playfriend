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
            <div className='hero-div'>
                <div className='hero-div-center'>
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
                </div>
            </div>

            <hr></hr>

            <div className='content'>
                <div className='content-header'>
                    Play minigames with friends!
                    <p>Playfriend is a developing chat bot that allows members of your server to play minigames together.</p>
                </div>
                <div className='content-div-left'>
                    <p>New minigames are currently in development and feature suggestions are welcome. Playfriend will also include random generators, helpful chat features, and more.</p>

                    <p>Try out Playfriend with a demo!</p>
                    <button disabled onClick={handleClick_demo}> Coming Soon </button>
                </div>

                <div className='content-div-left content-image'>
                </div>
            </div>

            <hr></hr>

            <div className='content'>
                <div className='content-header'>
                    Features
                    <p>Current and planned games, chat functions, and more.</p>
                </div>

                <div className='content-div-left'>
                    <p>New minigames are currently in development and feature suggestions are welcome. Playfriend will also include random generators, helpful chat features, and more.</p>

                </div>

                <div className='content-div-left'>
                    <p>New minigames are currently in development and feature suggestions are welcome. Playfriend will also include random generators, helpful chat features, and more.</p>

                </div>
            </div>

            <hr></hr>

            <div className='content-single'>
                <div className='content-header extra-header-margin'>
                    Game Log
                    <p>Records and rankings for available minigames!</p>
                </div>

                <div className='content-div-left'>
                    <p>New minigames are currently in development and feature suggestions are welcome. Playfriend will also include random generators, helpful chat features, and more.</p>

                </div>
            </div>

            <hr></hr>

            <div className='content-single'>
                <div className='content-header extra-header-margin'>
                    Contact
                    <p>Submit bug reports, feature suggestions, and feedback.</p>
                </div>

                <div className='content-div-left'>
                    <p>New minigames are currently in development and feature suggestions are welcome. Playfriend will also include random generators, helpful chat features, and more.</p>

                </div>
            </div>

        </div>
    );
}

export default Main;
