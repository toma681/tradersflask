import {
	Table,
	Thead,
	Tbody,
	Tfoot,
	Tr,
	Th,
	Td,
	TableCaption,
} from '@chakra-ui/react';
import { Box, Heading, Center } from '@chakra-ui/react';

import styles from '../../styles/styles';

export const PnL = ({ players, positions, truePnl, currentPlayer }) => {
	return (
		<Box
			rounded="md"
			bg={styles.lightBlueOpaque}
			py="6"
			px="10"
			width="60%"
			color={styles.white}
		>
			<Center mb="1.7vw">
				<Heading size="md" textAlign="center" style={styles.subtitle}>
					{currentPlayer}'s Turn
				</Heading>
			</Center>

			{generateTable({ players, positions, truePnl })}
		</Box>
	);
};

// assumes there is at least one round played
function generateTable({ players, positions, truePnl }) {
	// check if we have any values yet
	if (!(Object.keys(players).length === 0)) {
		return (
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
						<Td
							isNumeric
							pb="1vw"
							pt="0"
							px="0"
							pr="10px"
							style={{ ...styles.subtitle2, textAlign: 'center' }}
						>
							Position
						</Td>
						<Td
							isNumeric
							pb="1vw"
							pt="0"
							px="0"
							pr="10px"
							style={{ ...styles.subtitle2, textAlign: 'center' }}
						>
							True PnL
						</Td>
					</Tr>
				</Thead>
				<Tbody>
					{Object.keys(players).map((row) => (
						<Tr>
							{/* Name of player */}
							<Td
								pb="0.5vw"
								px="0"
								style={{ ...styles.regular, textAlign: 'left' }}
							>
								{players[row]}
							</Td>
							<Td
								pb="0.5vw"
								px="0"
								style={{ ...styles.regular, textAlign: 'center' }}
								isNumeric
							>
								{positions[row]}
							</Td>
							<Td
								pb="0.5vw"
								px="0"
								style={{ ...styles.regular, textAlign: 'center' }}
								isNumeric
							>
								{truePnl[row]}
							</Td>
						</Tr>
					))}
				</Tbody>
			</Table>
		);
	} else {
		// if there are no values yet return just the header
		return (
			<Table variant="unstyled" fontSize="small" size="sm">
				<Tbody>
					{/* First Row with column labels */}
					<Tr>
						<Th>Player</Th>
						<Th isNumeric>Position PnL</Th>
						<Th isNumeric>True PnL</Th>
					</Tr>
				</Tbody>
			</Table>
		);
	}
}

// TODO make fancy colors for positive/neg pnls
// function getColor(val) {
//   const colors = ["yellow", "red.100", "red.200", "green.100", "green.300"]

//   let maxVal = Math.max(...transactionArray.flat(1));
//   let frac = val/maxVal;
//   var i;
//   for (i = 1; i <= 5; i++) {
//     if (Math.abs(i/5 - frac) <= .19) {
//       return colors[i-1];
//     }
//   }
//   return colors[0];
// }
