import logoCircle from './images/pf_icon_complete.svg';
import textShort from './images/pf_text_short.svg';
import textLong from './images/pf_text.svg';
import ContactForm from './ContactForm';
import GameLog from './GameLog';
import { useEffect, useState } from 'react';


function Main() {

    const [status, setStatus] = useState('Online');
    const [percentUptime, setPercentUptime] = useState(99);

    // set timer for 5 minutes to get information from uptime robot about status of bot
    useEffect(() => {
        if (percentUptime === 99) {
            getStatus();
        }
        const uptimeRobotInterval = setInterval(() => {getStatus();}, 300000);
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
            if (json.monitors[0].status < 3) {
                setStatus("Online");
            } else {
                setStatus("Offline");
            }
            setPercentUptime(json.monitors[0].custom_uptime_ratio);
        })
        .catch(e => console.log('Uptime Robot getStatus Error - ', e));
    };

    const handleClick_invite = () => {
        window.open("https://discord.com/oauth2/authorize?client_id=785345529722175498");
      };

    const handleClick_demo = () => {
        window.open("https://discord.com/oauth2/authorize?client_id=785345529722175498");
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
                        <button className="button-shine button-mod" onClick={handleClick_invite}> Invite to Server
                        <div className="star star-1"></div>
                        <div className="star star-2"></div>
                        </button>
                    </div>
                </div>
            </div>

            <hr></hr>

            <div className='content-triple'>
                <div className='content-header content-header-3'>
                    Play minigames with friends!
                    <p>Playfriend is a developing chat bot that allows members of your server to play minigames together.</p>
                </div>

                <div className='content-div-left center'>
                    <div id="status-container">
                    <div id="status">
                        <h3>Current Status:</h3>
                        <div style={{color: status==='Online' ? '#32de84' : 'red'}}>
                            <div id='status-circle' style={{backgroundColor: status==='Online' ? '#32de84' : 'red'}}></div>
                            {status}
                        </div>
                    </div>
                        <div id="status-7-days">
                        <p>Playfriend has had <span style={{color: percentUptime > 70 ? '#32de84' : 'red'}}>{percentUptime}%</span> uptime in the last 7 days.</p>
                        </div>
                    </div>
                </div>

                <div className='content-div-left'>
                    <p>New minigames are currently in development and feature suggestions are welcome. </p>

                    <p>Try out Playfriend with a demo!</p>
                    <button id="demo-button" disabled onClick={handleClick_demo}> Coming Soon </button>
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

                <div className='gamelog-modifier'>
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
