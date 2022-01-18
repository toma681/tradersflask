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
} from '@chakra-ui/react';

/**
 *
 * @param {*} transactionArray a nested array of all the transactions,
 *  formatted such that transactionArray[1][2] is player two trading with player one
 * @param {*} names a list of names of players, with indices corresponding to @param transactionArray indices
 */
export const TransactionTable = ({ transactionArray, names }) => {
	const colors = ['yellow', 'blue.100', 'blue.200', 'green.100', 'green.300'];

	function getColor(val) {
		let maxVal = Math.max(...transactionArray.flat(1));
		let frac = val / maxVal;
		var i;
		for (i = 1; i <= 5; i++) {
			if (Math.abs(i / 5 - frac) <= 0.19) {
				return colors[i - 1];
			}
		}
		return colors[0];
	}

	return (
		<Table variant="simple" fontSize="x-small" h="350px" w="364px">
			<Tbody>
				{/* First Row with names */}
				<Tr>
					<Th></Th>
					{names.map((name) => (
						<Th>{names.indexOf(name)}</Th>
					))}
				</Tr>
				{/* Rest of rows with information */}
				{transactionArray.map((row) => (
					<Tr>
						<Th>{transactionArray.indexOf(row)}</Th>
						{row.map((transact) => (
							<Td bgColor={transact === 0 ? 'white' : getColor(transact)}>
								{transact !== 0 ? transact : null}
							</Td>
						))}
					</Tr>
				))}
			</Tbody>
		</Table>
	);
};
