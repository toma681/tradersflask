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

export const PnL = ({ players, pnl }) => {
	const headings = ['Q1', 'Q2', 'Q3', 'R1', 'R2', 'R3', 'R4', 'True', 'Total'];

	return (
		<Box
			rounded="lg"
			bg={styles.lightBlueOpaque}
			my="1.5vw"
			py="1.2vw"
			px="6"
			width="49%"
			ml="1%"
			color={styles.white}
		>
			<Center mb="1.7vw">
				<Heading size="md" style={styles.subtitle}>
					Profit and Loss
				</Heading>
			</Center>

			<Table variant="unstyled" fontSize="small" size="sm">
				<Tbody>
					{/* First Row with column labels */}
					<Tr>
						{/*<Th px="0" pr="10px" pb="1.2rem" style={styles.subtitle2}>*/}
						{/*	Player*/}
						{/*</Th>*/}
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
					</Tr>
					{/* Rest of rows with information */}
					{pnl.map((row) => (
						<Tr>
							{/* Name of player */}
							{/*<Th pb="0.8rem" px="0" style={styles.regular}>*/}
							{/*	{players[pnl.indexOf(row)]}*/}
							{/*</Th>*/}
							{Array.from(Array(9), (e, i) => {
								return (
									<Td
										isNumeric
										pb="0.5vw"
										px="0"
										style={{ ...styles.regular, textAlign: 'right' }}
										key={i}
									>
										{row[i]}
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
