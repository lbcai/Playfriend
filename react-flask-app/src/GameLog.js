import { useTable } from 'react-table';
import { useMemo, useState } from 'react';
import './GameLog.css';

function GameLog () {

    const [data, setData] = useState([{
        'key': '',
        '0': '',
        '1': '',
        '2': '',
    }]);

    useMemo(() => {
        fetch('/tictactoe')
        .then((response) => response.json())
        .then((json) => {
            console.log('json', json);
            let arrayOfObjects = Object.keys(json).map(key => {
                let array = json[key];
                array.key = key;
                return array;
             })
            arrayOfObjects.sort((a, b) => b[0] - a[0]);
            console.log('sorted', arrayOfObjects);
            setData(arrayOfObjects);
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
            Header: 'Rank',
            accessor: 'rank',
        },
        {
            Header: 'Player',
            accessor: 'key',
        },
        {
            Header: 'Games Won',
            accessor: '0', // accessor is the "key" in the data
        },
        {
            Header: 'Games Lost',
            accessor: '1',
        },
        {
            Header: 'Games Tied',
            accessor: '2',
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
