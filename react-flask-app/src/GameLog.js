import { useTable } from 'react-table';
import { useMemo, useState } from 'react';

function GameLog () {

    const [data, setData] = useState([{
        'date': '',
        'player1': '',
        'player2': '',
        'winner': ''
    }]);

    useMemo(() => {
        fetch('/tictactoe')
        .then((response) => response.json())
        .then((json) => {
            setData(json);
        });
    }, []);

    const getHm = () => {
        fetch('/hangman')
        .then((response) => response.json())
        .then((json) => {
            console.log(json);
        });
    };

    const columnsTtt = useMemo(
        () => [
        {
            Header: 'Date',
            accessor: 'date',
        },
        {
            Header: 'Player 1',
            accessor: 'player1', // accessor is the "key" in the data
        },
        {
            Header: 'Player 2',
            accessor: 'player2',
        },
        {
            Header: 'Winner',
            accessor: 'winner',
        },
        ],
        []
      );

    const tableInstance = useTable({ columns: columnsTtt, data });
    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
        } = tableInstance;

    return (
        <table {...getTableProps()}>

        <thead>
            {headerGroups.map(headerGroup => (                      // loop over header rows and apply header row props in tr
                <tr {...headerGroup.getHeaderGroupProps()}>
                    {headerGroup.headers.map(column => (            // loop over headers in each row and apply header cell props
                        <th {...column.getHeaderProps()}>
                            {column.render('Header')}
                        </th>))}
                </tr>))}
        </thead>

        <tbody {...getTableBodyProps()}>
          {rows.map(row => {
            prepareRow(row)
            return(
                <tr {...row.getRowProps()}>
                    {row.cells.map(cell=> {
                        return(
                            <td {...cell.getCellProps()}>
                                {cell.render('Cell')}
                            </td>
                        )
                    })}
                </tr>
            )
          })}
        </tbody>
      </table>
    );

}

export default GameLog;
