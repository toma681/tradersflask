import React from 'react';
import {
	Table,
	Thead,
	Tbody,
	Tfoot,
	Tr,
	Th,
	Td,
	TableCaption,
	HStack,
	Center,
	Flex,
	Text,
	Box,
	VStack,
	color,
	Heading,
} from '@chakra-ui/react';

import styles from '../../styles/styles';

/**
 *
 * @param {*} transactionArray a nested array of all the transactions
 * @param {*} names a list of names of players, with indices corresponding to @param transactionArray indices
 */
export const TransactionTable = ({
	transactionArray,
	names,
	avgTransaction,
}) => {
	// TODO change colors maybe make it scale granularly
	// TODO make table independent (maxVal is based on max of all tables right now)

	// Yellow, blue, darker blue, green, darker green
	const colors = [
		styles.yellow,
		styles.lightRed,
		styles.red,
		styles.lightGreen,
		styles.green,
	];

	const getColor = (val) => {
		let numVal = Number(val.split('x')[0]);
		let transactionPrices = transactionArray.flat(1).flat(1);
		for (let i = 0; i < transactionPrices.length; i++) {
			transactionPrices[i] = Number(transactionPrices[i].split('x')[0]);
		}
		let maxVal = Math.max(...transactionPrices);
		let frac = numVal / maxVal;
		var i;
		// TODO change how colors are calculated
		for (i = 1; i <= 5; i++) {
			if (Math.abs(i / 5 - frac) <= 0.19) {
				return colors[i - 1];
			}
		}
		return colors[0];
	};

	const round = (i, j, width) => {
		const amount = '20%';
		if (i === 0 && j === 0) {
			return { borderTopLeftRadius: amount };
		} else if (i === 0 && j === width - 1) {
			return { borderTopRightRadius: amount };
		} else if (i === width - 1 && j === 0) {
			return { borderBottomLeftRadius: amount };
		} else if (i === width - 1 && j === width - 1) {
			return { borderBottomRightRadius: amount };
		}
		return {};
	};

	return (
		<Flex justify="space-between">
			{transactionArray.map((question, i) => (
				<Box
					rounded="lg"
					bg={styles.lightBlueOpaque}
					py="6"
					px="2"
					pb="2vw"
					width="30%"
					color={styles.white}
				>
					<Center mb=".5vw">
						<Heading size="md" style={styles.subtitle}>
							Transactions
						</Heading>
					</Center>
					<Text mb="1.1vw" textAlign="center" style={styles.subtitle2}>
						Q{i + 1} Avg: {avgTransaction[i]}
					</Text>
					<Center>
						<Table
							variant="unstyled"
							fontSize="small"
							h="22vw"
							w="22vw"
							mx="1%"
							color="black"
							border="3px solid green"
						>
							<Tbody>
								{/* First Row with names */}
								<Tr>
									<Th></Th>

									{names.map((name, i) => (
										<Td
											color="white"
											py="0"
											pb=".75vw"
											height="30px"
											style={{ ...styles.miniRegular, textAlign: 'center' }}
											key={i}
										>
											{name}
										</Td>
									))}
								</Tr>
								{/* Rest of rows with information */}
								{question.map((row, i) => (
									<Tr>
										<Td
											color="white"
											px="0"
											pr=".5vw"
											width="30px"
											style={{ ...styles.miniRegular, textAlign: 'center' }}
										>
											{names[question.indexOf(row)]}
										</Td>

										{row.map((transact, j) => (
											<Td
												bgColor={
													transact === 0
														? 'rgba(203, 247, 237, 0.1)'
														: getColor(transact)
												}
												px="0"
												style={{
													...styles.miniRegular,
													textAlign: 'center',
													...round(i, j, row.length),
												}}
											>
												{transact !== 0 ? transact : null}
											</Td>
										))}
									</Tr>
								))}
							</Tbody>
						</Table>
					</Center>
				</Box>
			))}
		</Flex>
	);
};
