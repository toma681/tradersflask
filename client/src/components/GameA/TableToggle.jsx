import React, { useState } from 'react';
import {
	Table,
	Thead,
	Tr,
	Th,
	Td,
	TableCaption,
	Flex,
	Box,
	Button,
	Spacer,
} from '@chakra-ui/react';

import { TransactionTable } from './TableToggleComponents/TransactionTable';
import { SpreadTable } from './TableToggleComponents/SpreadTable';

/**
 *
 * @param transactions:
 * @param names:
 * @param questions:
 * @param spreads:
 *
 */
export const TableToggle = ({ transactions, names, questions, spreads }) => {
	const [showSpreads, setShowSpreads] = useState(false);

	let tables;
	let caption;

	// Logic for switching tables
	if (showSpreads) {
		tables = transactions.map((singleAssetTransactions) => (
			<TransactionTable
				transactionArray={singleAssetTransactions}
				names={names}
			/>
		));
		caption = 'Transactions';
	} else {
		tables = spreads.map((singleSpread) => (
			<SpreadTable spreads={singleSpread} names={names} />
		));
		caption = 'Spreads';
	}

	return (
		<Box borderWidth="1px" borderRadius="lg" padding="10px">
			<Flex flexDir="column" alignItems="center">
				<Table variant="simple" size="1200px" fontSize="medium">
					<TableCaption fontSize="xl" padding="5px">
						{caption}
					</TableCaption>
					<Thead>
						{/* Puts questions in the header */}
						<Tr>
							{questions.map((question) => (
								<Th fontSize="small">{question}</Th>
							))}
						</Tr>
					</Thead>
					{/* Creates tables for each question */}
					<Tr>
						{tables.map((tab) => (
							<Td>{tab}</Td>
						))}
					</Tr>
				</Table>
				{/* Toggle which table is shown */}
				<Button
					onClick={() => setShowSpreads(!showSpreads)}
					colorScheme="teal"
					w="100px"
				>
					Toggle Info
				</Button>
			</Flex>
		</Box>
	);
};
