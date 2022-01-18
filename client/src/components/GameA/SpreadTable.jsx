import {
	Table,
	Thead,
	Tbody,
	Tr,
	Th,
	Td,
	Box,
	Center,
	Heading,
} from '@chakra-ui/react';

import styles from '../../styles/styles';

/**
 * The table of each player's spread
 * @param {spreads} props json formatted list of spreads to put in the table
 */
export const SpreadTable = ({ spreads, names }) => {
	const headings = ['Q1 Bid', 'Q1 Ask', 'Q2 Bid', 'Q2 Ask', 'Q3 Bid', 'Q3 Ask'];

	return (
		<Box
			rounded="lg"
			bg={styles.lightBlueOpaque}
			my="1.5vw"
			py="1.2vw"
			px="6"
			width="49%"
			mr="1%"
			color={styles.white}
		>
			<Center mb="1.7vw">
				<Heading size="md" style={styles.subtitle}>
					Spreads
				</Heading>
			</Center>

			<Table variant="unstyled" fontSize="small" size="sm">
				<Thead>
					<Tr>
						<Td
							pt="0"
							pb="1vw"
							px="0"
							pr="10px"
							style={{ ...styles.subtitle2, textAlign: 'left' }}
						>
							Player
						</Td>
						{headings.map((heading, i) => (
							<Td
								isNumeric
								pb="0.8vw"
								pt="0"
								px="0"
								style={{ ...styles.subtitle2, textAlign: 'right' }}
								key={i}
							>
								{heading}
							</Td>
						))}
					</Tr>
				</Thead>
				<Tbody>
					{/* Create all the player spread elements */}
					{spreads.map((spread) => (
						<Tr>
							<Td
								pb="0.5vw"
								px="0"
								isNumeric
								style={{ ...styles.regular, textAlign: 'left' }}
							>
								{names[spreads.indexOf(spread)]}
							</Td>

							{Array.from(Array(6), (e, i) => {
								return (
									<Td
										isNumeric
										pb="0.5vw"
										px="0"
										style={{ ...styles.regular, textAlign: 'right' }}
										key={i}
									>
										{spread[i]}
									</Td>
								);
							})}
						</Tr>
					))}
				</Tbody>
			</Table>
		</Box>
	);
};
