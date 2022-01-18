import React, { useState, useEffect } from 'react';

import axios from 'axios';

import {
	Button,
	Flex,
	Modal,
	ModalOverlay,
	ModalContent,
	useDisclosure,
	Stack,
	NumberInput,
	NumberInputField,
} from '@chakra-ui/react';

/**
 * @returns button to set new spread
 */
const SetSpread = ({ spread, setSpread }) => {
	const [low, setLow] = useState(spread[0]);
	const [high, setHigh] = useState(spread[1]);
	const [method, setMethod] = useState('');
	const { isOpen, onOpen, onClose } = useDisclosure();

	useEffect(() => {
		setLow(spread[0]);
		setHigh(spread[1]);
	}, [spread, isOpen]);

	const submit = async () => {
		if (method) {
			let quantity = 0;
			if (method === 'BUY') {
				quantity = spread[1];
			} else if (method === 'SELL') {
				quantity = spread[0];
			}

			await axios
				.post('http://127.0.0.1:5000/GameB/transact', {
					user: {
						username: 'test@test.com',
						secret_key: 'gjfhxc',
					},
					position: method,
					quantity: quantity,
				})
				.then((res) => {
					console.log(res);
				});
		}

		await axios
			.post('http://127.0.0.1:5000/GameB/makeMarket', {
				user: {
					username: 'test@test.com',
					secret_key: 'gjfhxc',
				},
				bid: low,
				bid_lots: 1,
				ask: high,
				ask_lots: 1,
			})
			.then((res) => console.log(res));

		setSpread([low, high]);
		onClose();
	};

	let modal = (
		<Modal isOpen={isOpen} onClose={onClose}>
			<ModalOverlay />
			<ModalContent>
				<Stack spacing={4} direction="column" align="center" margin="10px">
					<text>
						<b>Set New Spread</b>
					</text>

					<text onClick={() => console.log(method)}>Input Low</text>
					<NumberInput value={low} width="200px">
						<NumberInputField onChange={(e) => setLow(e.target.value)} />
					</NumberInput>

					<text>Input High</text>
					<NumberInput value={high} width="200px">
						<NumberInputField onChange={(e) => setHigh(e.target.value)} />
					</NumberInput>

					<Button onClick={submit}>Submit</Button>
				</Stack>
			</ModalContent>
		</Modal>
	);

	return (
		<>
			{modal}
			<Flex mb="1rem">
				<Button
					colorScheme="orange"
					size="lg"
					onClick={() => {
						setMethod('BUY');
						onOpen();
					}}
					mr="1rem"
				>
					Buy Previous
				</Button>

				<Button
					colorScheme="orange"
					size="lg"
					onClick={() => {
						setMethod('SELL');
						onOpen();
					}}
					ml="1rem"
				>
					Sell Previous
				</Button>
			</Flex>
			<Button
				colorScheme="gray"
				size="lg"
				onClick={() => {
					setMethod('');
					onOpen();
				}}
			>
				Set New Spread
			</Button>
		</>
	);
};

export default SetSpread;
