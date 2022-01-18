import React, { useEffect, useState } from 'react';

import Transactions from '../components/GameB/Transactions';
import SetSpread from '../components/GameB/SetSpread';
import axios from 'axios';

import { Box, Flex, Text, Heading } from '@chakra-ui/react';
import { PnL } from '../components/GameB/PnL';

import styles from '../styles/styles';
import Underline from '../img/underline.svg';

function chunkCards(cards) {
	var i,
		j,
		temparray,
		chunk = 13;
	var ret = [];
	for (i = 0, j = cards.length; i < j; i += chunk) {
		temparray = cards.slice(i, i + chunk);
		ret.push(temparray);
	}
	return ret;
}

const GameB = () => {
	const [range, updateRange] = useState({ low: 1, high: 50 });
	const [spread, setSpread] = useState({
		ask: { price: 100, volume: 100 },
		bid: { price: 0, volume: 100 },
	});
	const [cards, updateCards] = useState([]);
	const [turns, updateTurns] = useState([]);
	const [pnltable, updatePnLTable] = useState([]);
	const [positions, updatePositions] = useState({});
	const [truePnl, updateTruePnL] = useState({});
	const [players, updatePlayers] = useState({
		0: 'p0',
		1: 'p1',
		2: 'p2',
		3: 'p3',
		4: 'p4',
	});
	const [currentPlayer, updateCurrentPlayer] = useState(
		'default current player'
	);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameB/revealedCards')
			.then((res) => updateCards(res.data));
	}, [cards]);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameB/range')
			.then((res) => updateRange(res.data));
	}, [range]);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameB/turnList')
			.then((res) => updateTurns(res.data));
	}, [turns]);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameB/spread')
			.then((res) => setSpread(res.data));
	}, [spread]);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameB/players')
			.then((res) => updatePlayers(res.data));
	}, [players]);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameB/playerPositions')
			.then((res) => updatePositions(res.data));
	}, [positions]);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameB/truePnl')
			.then((res) => updateTruePnL(res.data));
	}, [truePnl]);

	useEffect(() => {
		axios
			.get('http://127.0.0.1:5000/GameB/currentPlayer')
			.then((res) => updateCurrentPlayer(res.data));
	});

	// TODO change layout so it's wider, maybe fixed scroll box for turns
	return (
		<Box
			display="flex"
			flexDirection="column"
			alignItems="center"
			bg={styles.darkerBlue}
			px="14"
			py="12"
			backgroundImage="url('/bg.png')"
			backgroundPosition="center"
			backgroundRepeat="no-repeat"
			backgroundSize="100% 100%"
			minHeight="100vh"
			color={styles.white}
		>
			<Flex direction="column" align="center" width="100%">
				<Heading color={styles.white} mb="-1vw" style={styles.title}>
					Game B
				</Heading>
				<img src={Underline} alt="" width="23%" />
			</Flex>
			<Text mt="1vw" style={styles.subtitle2}>
				Bid: ${spread['bid']['price']} x {spread['bid']['volume']}, Ask: $
				{spread['ask']['price']} x {spread['ask']['volume']}
			</Text>
			<Text style={styles.subtitle2}>
				Card Range: {range['low']} to {range['high']}
			</Text>

			<Transactions turns={turns} />

			<Flex px="0" w="80%">
				<PnL
					players={players}
					positions={positions}
					truePnl={truePnl}
					currentPlayer={currentPlayer}
				/>

				<Flex direction="column" justify="center" w="40%" align="center">
					<Text fontSize="xl" style={styles.subtitle}>
						Cards Revealed
					</Text>
					{/* TODO make prettier */}
					<Text style={styles.regular}>
						{cards.length
							? chunkCards(cards).map((chunk) => (
									<>
										{' '}
										{chunk.toString()} <br></br>{' '}
									</>
							  ))
							: '-'}
					</Text>
				</Flex>
			</Flex>

			{/* <BuySellButtons /> */}
			{/* <SetSpread spread={spread} setSpread={setSpread} /> */}
		</Box>
	);
};

export default GameB;
