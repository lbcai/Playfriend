function GameLog () {

    const getTtt = () => {
        fetch('/tictactoe')
        .then((response) => response.json())
        .then((json) => {
            console.log(json);
        });
    };

    const getHm = () => {
        fetch('/hangman')
        .then((response) => response.json())
        .then((json) => {
            console.log(json);
        });
    };

    return (
        <div>
        </div>
    );

}

export default GameLog;
