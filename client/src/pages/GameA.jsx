import React, { useEffect, useState } from 'react';
import { Flex, Center, Box, Heading, Text } from '@chakra-ui/react';
import axios from 'axios';

// Our Components
// import { UserInput } from '../components/GameA/UserInput';
// import { TableToggle } from '../components/GameA/TableToggle';
import { SpreadTable } from '../components/GameA/SpreadTable';
import { TransactionTable } from '../components/GameA/TransactionTable';
// import { Timer } from '../components/GameA/Timer';
import { PnL } from '../components/GameA/PnL';
// import { Login } from '../components/Utils/Login';
// import { CardHub } from '../components/Utils/CardHub';

import styles from '../styles/styles';
import Underline from '../img/underline.svg';

const GameA = () => {
	const [players, updatePlayers] = useState(['p0', 'p1', 'p2']);
	const [transactions, updateTransactions] = useState([
		[
			['0', '20x5', '10.5x5'],
			['8x15', '0', '20.5x7'],
			['10.5x1', '18x16', '0'],
		],
		[
			['0', '8x3', '5x10'],
			['4x15', '0', '8x8'],
			['3x12', '25x9', '0'],
		],
		[
			['0', '1x5', '2x2'],
			['9x15', '0', '21x5'],
			['9x20', '22x6', '0'],
		],
	]);
	const [market, updateMarket] = useState([
		['99.0x1', '99.0x1', '99.0x2', '99.0x2', '99.0x3', '99.0x4'],
		['5.0x1', '10.0x1', '50.0x2', '100.0x2', '100.0x3', '200.0x4'],
		['5.0x1', '10.0x1', '50.0x2', '100.0x2', '100.0x3', '200.0x4'],
	]);
	const [pnl, updatePnl] = useState([
		[1, 2, 3, 4, 5, 6, 7, 8, 9],
		[9, 8, 7, 6, 5, 4, 3, 2, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1],
	]);
	const [avgTransaction, updateAvgTransaction] = useState([10, 20, 300]);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameA/players')
			.then((res) => updatePlayers(res.data));
	}, [players]);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameA/transaction')
			.then((res) => updateTransactions(res.data));
	}, [transactions]);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameA/market')
			.then((res) => updateMarket(res.data));
	}, [market]);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameA/pnl')
			.then((res) => updatePnl(res.data));
	}, [pnl]);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameA/avgTransaction')
			.then((res) => updateAvgTransaction(res.data));
	}, [avgTransaction]);

	return (
		<Box
			direction="column"
			bg={styles.darkerBlue}
			px="14"
			py="12"
			backgroundImage="url('/bg.png')"
			backgroundPosition="center"
			backgroundRepeat="no-repeat"
			backgroundSize="100% 100%"
			minHeight="100vh"
		>
			<Flex direction="column" align="center">
				<Heading color={styles.white} mb="-1vw" style={styles.title}>
					Game A
				</Heading>
				<img src={Underline} alt="" width="23%" />
			</Flex>
			{/* <Flex flexDir="column">
						<UserInput />
						<Timer time={1} onTimeOut={()=> alert("Times Up!")}/>
					</Flex> */}
			<Flex>
				<SpreadTable spreads={market} names={players} />
				<PnL players={players} pnl={pnl} />
			</Flex>

			{/* Uncomment the next line to see the spread/transaction tables */}
			{/* <TableToggle
					transactions={transactions}
					questions={questions}
					names={names}
					spreads={allSpreads}
				/> */}

			<TransactionTable
				transactionArray={transactions}
				names={players}
				avgTransaction={avgTransaction}
			/>

			{/* <CardHub available_games={games} game="Game A" /> */}
		</Box>
	);
};

export default GameA;
