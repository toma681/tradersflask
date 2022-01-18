import React from 'react';

import {
	Box,
	Center,
	Heading,
	Table,
	Thead,
	Tbody,
	Tr,
	Th,
	Td,
	TableCaption,
} from '@chakra-ui/react';

import styles from '../../styles/styles';

/**
 * @param playerNames - list of playerNames
 * @param Lows - list of lows in spreads set
 * @param Highs - list of highs in spreads set
 * @param Actions - list of actions taken
 * @returns table displaying transaction history
 */
const Transactions = ({ turns }) => {
	const headings = ['Bid', 'Bid Size', 'Ask', 'Ask Size'];

	const attributes = ['name', 'bid', 'bid_size', 'ask', 'ask_size', 'action'];

	return (
		<Box
			rounded="md"
			bg={styles.lightBlueOpaque}
			my="9"
			py="6"
			px="10"
			width="80%"
			color={styles.white}
		>
			<Center mb="1.7vw">
				<Heading size="md" style={styles.subtitle}>
					Transaction History
				</Heading>
			</Center>

			<Table variant="unstyled" fontSize="small" size="sm">
				<Thead>
					<Tr>
						<Td
							pb="1vw"
							pt="0"
							px="0"
							pr="10px"
							style={{ ...styles.subtitle2, textAlign: 'left' }}
						>
							Player Name
						</Td>

						{headings.map((heading, i) => (
							<Td
								isNumeric
								pb="1vw"
								pt="0"
								px="0"
								style={{ ...styles.subtitle2, textAlign: 'right' }}
								key={i}
							>
								{heading}
							</Td>
						))}

						<Td
							pb="1vw"
							pt="0"
							px="0"
							style={{ ...styles.subtitle2, textAlign: 'right' }}
						>
							Action
						</Td>
					</Tr>
				</Thead>
				<Tbody>
					{turns.slice(0, 6).map((turn) => (
						<Tr>
							{attributes.map((attr, i) => (
								<Td
									pb="0.5vw"
									px="0"
									style={{
										...styles.regular,
										textAlign: i === 0 ? 'left' : 'right',
									}}
									key={i}
								>
									{turn[attr]}
								</Td>
							))}
						</Tr>
					))}
				</Tbody>
			</Table>
		</Box>
	);
};

export default Transactions;
