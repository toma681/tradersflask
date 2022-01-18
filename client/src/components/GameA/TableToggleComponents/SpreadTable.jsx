import { Table, Thead, Tbody, Tr, Th, Td } from '@chakra-ui/react';
/**
 * The table of each player's spread
 * @param {spreads} props json formatted list of spreads to put in the table
 */
export const SpreadTable = ({ spreads, names }) => {
	return (
		<Table variant="simple" fontSize="small" h="350px" w="364px">
			<Thead>
				<Tr>
					<Th>Player</Th>
					<Th isNumeric>Ask</Th>
					<Th isNumeric>Bid</Th>
				</Tr>
			</Thead>
			<Tbody>
				{/* Create all the player spread elements */}
				{spreads.map((player) => (
					<Tr key={player.key}>
						<Td>{names[player.key]}</Td>
						<Td isNumeric>{player.low}</Td>
						<Td isNumeric>{player.high}</Td>
					</Tr>
				))}
			</Tbody>
		</Table>
	);
};
