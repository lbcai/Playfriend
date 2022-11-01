import logoCircle from './images/pf_icon_complete.svg';
import textShort from './images/pf_text_short.svg';
import textLong from './images/pf_text.svg';
import ContactForm from './ContactForm';
import GameLog from './GameLog';
import { scroller } from 'react-scroll';
import { useEffect, useState } from 'react';


function Main() {

    const [status, setStatus] = useState('');

    // set timer for 5 minutes to get information from uptime robot about status of bot
    useEffect(() =>{
        const uptimeRobotInterval = setInterval(() => {getStatus();}, 15000);
        // always clean up intervals
        return () => {clearInterval(uptimeRobotInterval);};
    }, []);

    const getStatus = () => {
        fetch('/status', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: ''
        })
        .then(response => response.json())
        .then(json => {
            if (json.stat === "ok") {
                setStatus("online");
            } else {
                setStatus("offline");
            }

        })
        .catch(e => console.log('Uptime Robot getStatus Error - ', e));
    };

    const handleClick_invite = () => {
        window.open("https://discord.com/oauth2/authorize?client_id=785345529722175498&permissions=470080&scope=bot");
      };

    const handleClick_demo = () => {
    window.open("https://discord.com/oauth2/authorize?client_id=785345529722175498&permissions=470080&scope=bot");
    };

    const scrollToTop = () => {
        scroller.scrollTo('navBackground', {
            duration: 500,
            delay: 0,
            smooth: "easeInOutQuart",
          });
      }

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
                        <div className='status-text'>
                            Playfriend is currently {status}.
                        </div>
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

            <div className='content' id='features'>
                <div className='content-header'>
                    Features
                    <p>Current and planned games, chat functions, and more.</p>
                </div>

                <div className='content-div-left left-align'>
                    <p>🎲 Current Features:</p>
                    <ul className='ul1'>
                        <li>Tic-Tac-Toe
                            <ul>
                                <li>Singleplayer against Minimax AI</li>
                                <li>Multiplayer against another server member</li>
                                <li>Customizable XO markers</li>
                                <li>Difficulty settings for singleplayer mode</li>
                            </ul>
                        </li>

                        <li>Hangman
                            <ul>
                                <li>Flexible player count (1+)</li>
                                <li>Optional custom word/phrase submissions</li>
                            </ul>
                        </li>

                        <li>
                            >help Command
                            <ul>
                                <li>Dynamic command display based on current game state</li>
                            </ul>
                        </li>

                    </ul>
                </div>

                <div className='content-div-left left-align'>
                    <p>🔒 Upcoming Features:</p>
                    <ul style={{paddingBottom: 20}} className='ul2'>
                        <li>Dungeon Crawler (Working Title)
                            <ul>
                                <li>1-8 player procedurally generated dungeon exploration roleplaying game</li>
                                <li>Variety of classes to choose from</li>
                                <li>Variety of challenging puzzles, boss fights, and random encounters</li>
                                <li>Upgrade your character with skill trees and items</li>
                                <li>Sprites and custom graphics included</li>
                            </ul>
                        </li>

                        <li>Standard Chat Features
                            <ul>
                                <li>RemindMe function</li>
                                <li className='li-dice'>Random number generators</li>
                            </ul>
                        </li>
                    </ul>
                </div>
            </div>

            <hr></hr>

            <div className='content-single'  id='game-log'>
                <div className='content-header extra-header-margin'>
                    Game Log
                    <p>Records and rankings for available minigames!</p>
                </div>

                <div className='content-div-left'>
                    <p>Coming soon!</p>
                    <GameLog />
                </div>
            </div>

            <hr></hr>

            <div className='content-single' id='contact'>
                <div className='content-header extra-header-margin'>
                    Contact
                    <p>Submit bug reports, feature suggestions, and feedback.</p>
                </div>

                <div className='content-div-left'>

                <ContactForm />

                </div>
            </div>

        </div>
    );
}

export default Main;
