import React, { useState } from 'react';
import { Formik, Field, Form } from 'formik';
import {
	Text,
	Flex,
	Center,
	Box,
	Heading,
	FormControl,
	FormLabel,
	Input,
	Button,
	Spacer,
	VStack,
} from '@chakra-ui/react';
import axios from 'axios';

/**
 * Spread slector component, which changes the UserInput's spread state variable
 * @param {onClick} props Change Spread to a different value. Currently hard-coded
 */
export const SpreadSelector = (props) => {
	return (
		<Box
			borderColor="gray.200"
			borderWidth="1px"
			rounded="md"
			bg="white"
			p={[1, 8]}
			w="100%"
		>
			<Center>
				<Heading size="md">Choose Your Spread</Heading>
			</Center>
			<Flex style={{ padding: '4px' }}>
				<Text>Question 1</Text>
				<Flex colorScheme="teal">
					<Button
						colorScheme="teal"
						m="1"
						w="50px"
						onClick={() => props.onClick(5)}
						isDisabled
					>
						5
					</Button>
					<Button
						colorScheme="teal"
						m="1"
						w="50px"
						onClick={() => props.onClick(10)}
					>
						10
					</Button>
					<Button
						colorScheme="teal"
						m="1"
						w="50px"
						onClick={() => props.onClick(15)}
						isDisabled
					>
						15
					</Button>
				</Flex>
			</Flex>
			<Flex style={{ padding: '4px' }}>
				<Text>Question 2</Text>
				<Flex colorScheme="teal">
					<Button
						colorScheme="teal"
						m="1"
						w="50px"
						onClick={() => props.onClick(5)}
					>
						5
					</Button>
					<Button
						colorScheme="teal"
						m="1"
						w="50px"
						onClick={() => props.onClick(10)}
						isDisabled
					>
						10
					</Button>
					<Button
						colorScheme="teal"
						m="1"
						w="50px"
						onClick={() => props.onClick(15)}
						isDisabled
					>
						15
					</Button>
				</Flex>
			</Flex>
			<Flex style={{ padding: '4px' }}>
				<Text>Question 3</Text>
				<Flex colorScheme="teal">
					<Button
						colorScheme="teal"
						m="1"
						w="50px"
						onClick={() => props.onClick(5)}
						isDisabled
					>
						5
					</Button>
					<Button
						colorScheme="teal"
						m="1"
						w="50px"
						onClick={() => props.onClick(10)}
						isDisabled
					>
						10
					</Button>
					<Button
						colorScheme="teal"
						m="1"
						w="50px"
						onClick={() => props.onClick(15)}
					>
						15
					</Button>
				</Flex>
			</Flex>
		</Box>
	);
};

/**
 * Get's user's bid and ask values
 * @param {spread} props the spread passed in from UserInput's state variable
 */
export const ValueInput = (props) => {
	return (
		<Box
			borderColor="gray.200"
			borderWidth="1px"
			rounded="md"
			bg="white"
			p={[1, 8]}
			w="100%"
		>
			<Text style={{ 'text-align': 'center', 'font-weight': '800' }}>
				Enter your prices:
			</Text>
			<Formik
				initialValues={{ low: '', high: '', spread: props.spread }}
				onSubmit={async (values) => {
					if (validateSpread(values)) {
						// TODO submit real values to server through API
						axios.post('http://127.0.0.1:5000/setPlayerMarkets', {
							params: {
								"q1_low": 1,
								"q1_high": 20,
								"q2_low": 10,
								"q2_high": 15,
								"q3_low": 10,
								"q3_high": 25,
								"room_id": 12,
								"user_id": 1
							}
						})
							.then(function (response) {
								alert(response)
								console.log("setPlayerMarkets response: ");
								console.log(response);
						})
							.catch(function (error) {
								alert("An error has occured while submitting spreads: \n" + error)
								console.log(error);
						})
							.then(function () {
								// always executed
						});


						alert(JSON.stringify(values, null, 2));
					} else {
						alert('Error: Make sure spreads are entered correctly');
					}
				}}
			>
				<Form style={{ padding: '12px' }}>
					<Field
						name="low"
						type="number"
						placeholder="15"
						style={{
							border: '1px solid black',
							'border-radius': '6px',
							'margin-right': '4px',
							'text-align': 'right',
						}}
					/>
					<Field
						name="high"
						type="number"
						placeholder={15 + props.spread}
						style={{
							border: '1px solid black',
							'border-radius': '6px',
							'margin-right': '4px',
							'text-align': 'right',
						}}
					/>
					<Button type="submit">Submit</Button>
				</Form>
			</Formik>
			<Spacer />
			<Center>
				<Button
					colorScheme="red"
					mr="4"
					w="100px"
					onClick={() => props.onClick()}
					style={{ 'margin-bottom': '15px', padding: '12px' }}
				>
					Reset Spread
				</Button>
			</Center>
		</Box>
	);
};

/**
 * Parent function for above components. Controls which component is rendered.
 */
export const UserInput = () => {
	const [spread, setSpread] = useState(null);

	const [choseSpread, setChoseSpread] = useState(false);

	/**
	 * Change the value of the spread and render change choseSpread to true to render ValueInput
	 * @param {*} newSpread the value to change the spread to
	 */
	const changeSpread = (newSpread) => {
		setSpread(newSpread);
		setChoseSpread(true);
	};

	/**
	 * Reset choseSpread to allow user to re-choose their spread.
	 */
	const resetSpread = () => {
		setChoseSpread(false);
	};

	let inputElem;
	if (choseSpread) {
		inputElem = <ValueInput spread={spread} onClick={resetSpread} />;
	} else {
		inputElem = <SpreadSelector onClick={changeSpread} />;
	}
	return inputElem;
};

/**
 * Validate that the inputs are not blank and are the correct spread
 * @param {values} values the values object containing low, high, and spread values
 * @returns {boolean} true if inputs are correct and false otherwise
 */
function validateSpread(values) {
	if (values.high === '' || values.low === '') {
		return false;
	}
	if (values.high - values.low !== values.spread) {
		return false;
	}
	return true;
}
